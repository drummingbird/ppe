from openerp import models, fields, api
import datetime

class Bundle(models.Model):
    _name = 'mqo.bundle'
    
    name = fields.Char(string="Name")
    product_templates = fields.Many2many('product.template', relation='mqo_bundle_product_relation', string="Product templates")
    exercises = fields.Many2many('mqo.exercise', relation='mqo_bundle_exericse_relation', string="Exercises")


class BundleAllocation(models.Model):
    _name = 'mqo.bundle.allocation'
    
    bundle = fields.Many2one('mqo.bundle', string="Exercise bundle")
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    expiry_datetime = fields.Datetime(string="Expiry", default=lambda self: fields.Datetime.to_string(datetime.datetime.now() + datetime.timedelta(days=365)))
    
    @api.multi
    def _check_expiry(self):
        # Automatically raise warning when approaching expiry, and delete expired bundle allocations.
        warning_list_ids = []
        for r in self:
            current_datetime = datetime.datetime.now() 
            if current_datetime > r.expiry_datetime:
                r.unlink()
            elif current_datetime > r.expiry_datetime - datetime.timedelta(days=21):
                warning_list_ids.append(r.id)
        return warning_list_ids


    @api.model
    def allocateExercises_from_Bundles(self, partner_ids):
        # Create assignment id

        allocation_obj = self.env['mqo.allocation']
        # get list of currently allocated exercises:
        for partner_id in partner_ids:
            allocations = allocation_obj.search({'partner_id': partner_id})
            bundle_allocations = self.search({'partner_id': partner_id})
            exercise_id_list = []
            for allocation in allocations:
                exercise_id_list.append(allocation.exercise_id.id)
            
            print('Checking whether new exercises need to be allocated from bundles')
            for bundle_allocation in bundle_allocations:
                for exercise in bundle_allocation.bundle.exercises:
                    # see if allocation already exists, and update or create one if needed.
                    if exercise.id not in exercise_id_list:
                        allocation_obj.create({'partner_id': partner_id, 'exercise_id': exercise.id})
                        print('Exercises were allocated')
                    exercise_id_list.remove(exercise.id)
            
            
            # remove allocations for any remaining exercise_id_list entries, since they aren't in any of the allocated bundles.
            if len(exercise_id_list) > 0:
                print('Removing exercises no longer in any bundles')
                allocation_obj.search({'partner_id': partner_id, 'exercise_id': exercise_id_list}).unlink()
        

    @api.model
    def create(self, vals):
        try:
            res = super(BundleAllocation, self).create(vals)
        except ValueError:
            return res
        else:
            partner_id_list = []
            for bundle_allocation in res:
                partner_id_list.append(bundle_allocation.partner_id.id)
            partner_ids = set(partner_id_list)
            self.allocateExercises_from_Bundles(partner_ids)
        return res
    
