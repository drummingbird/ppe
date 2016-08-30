from openerp import models, fields, api
import datetime

class Bundle(models.Model):
    _name = 'mqo.bundle'
    
    name = fields.Char(string="Name")
    exercises = fields.Many2many('mqo.exercise', 'mqo_bundle_exericse_relation', 'bundle_id', 'exercise_id', string="Exercises")


class BundleAllocation(models.Model):
    _name = 'mqo.bundle.allocation'
    
    bundle = fields.Many2one('mqo.bundle', string="Exercise bundle")
    learner = fields.Many2one('mqo.learner', string="Learner", required=True)
    expiry_datetime = fields.Datetime(string="Expiry", default=lambda self: fields.Datetime.to_string(datetime.datetime.now() + datetime.timedelta(days=365)))
    
    @api.multi
    def _check_expiry(self):
        # Automatically raise warning when approaching expiry, and delete expired bundle allocations.
        warning_list_ids = []
        learner_list = []
        for r in self:
            current_datetime = datetime.datetime.now() 
            if current_datetime > r.expiry_datetime:
                learner_list.append(r.learner.id)
                r.unlink()
            elif current_datetime > r.expiry_datetime - datetime.timedelta(days=21):
                warning_list_ids.append(r.id)
        
        learners = set(learner_list)
        self.allocateExercises_from_Bundles(learners)
        return warning_list_ids

    @api.model
    def allocateExercises_from_Bundles(self, learners):
        # Create assignment id

        allocation_obj = self.env['mqo.allocation']
        # get list of currently allocated exercises:
        for learner in learners:
            allocations = allocation_obj.search([('learner', '=', learner)])
            bundle_allocations = self.search([('learner', '=', learner)])
            exercise_id_list = []
            for allocation in allocations:
                exercise_id_list.append(allocation.exercise_id.id)
            
            print('Checking whether new exercises need to be allocated from bundles')
            for bundle_allocation in bundle_allocations:
                for exercise in bundle_allocation.bundle.exercises:
                    # see if allocation already exists, and update or create one if needed.
                    if exercise.id not in exercise_id_list:
                        res = allocation_obj.create({'learner': learner, 'exercise_id': exercise.id})
                        print('Exercises were allocated')
                    else:
                        exercise_id_list.remove(exercise.id)
            
            
            # remove allocations for any remaining exercise_id_list entries, since they aren't in any of the allocated bundles.
            if len(exercise_id_list) > 0:
                print('Removing exercises no longer in any bundles')
                res = allocation_obj.search([('learner', '=', learner), ('exercise_id', 'in', exercise_id_list)]).unlink()
        

    @api.model
    def create(self, vals):
        try:
            res = super(BundleAllocation, self).create(vals)
        except ValueError:
            return res
        else:
            learner_list = []
            for bundle_allocation in res:
                learner_list.append(bundle_allocation.learner.id)
            learners = set(learner_list)
            self.allocateExercises_from_Bundles(learners)
        return res
    
