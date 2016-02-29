# -*- coding: utf-8 -*-
from openerp import fields, models, api
import datetime
import math

def sigmoid(t, c, r, e, down):
    return 1*down + (1 - 2*down)/(1 + math.pow(e, -(t-c)/r))

def expdec(t, c, r, e):
    return 1 - math.pow(e, -(t+c)/r)

class Mqo_exArr():
    exercise_id = 0
    suitability = 0
    score = 0
    
    def __init__(self, exercise_id, suitability, score):
        self.exercise_id = exercise_id
        self.suitability = suitability
        self.score = score
 
    def mod_Score(self, assignment):
        # modify score based on an recent assignment
        elapsed_timedelta = datetime.datetime.now() - fields.Datetime.from_string(assignment.datetime_allocated)
        # elapsed_timedelta_datum = datetime.datetime.now() # - some date
        t = elapsed_timedelta.days
        a = assignment.exercise_id
        d_sig = 1 - a.sig_m*sigmoid(t, a.sig_c, a.sig_r, a.sig_e, True)
        d_exp = max(1 - a.exp_m*(1 - expdec(t, a.exp_c, a.exp_r, a.exp_e)), 0)
        self.score = self.score * d_sig * d_exp


class Partner(models.Model):
    _inherit = 'res.partner'

    allocation_ids = fields.One2many('mqo.allocation', 'partner_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'partner_id', string="Assigned Exercises")
    
    next_exercise_id = fields.Many2one(comodel_name='mqo.exercise', store=True, readonly=True, compute='_compute_next_exercise', string="Next Exercise")
    
    @api.depends('allocation_ids', 'assignment_ids')
    def _compute_next_exercise(self):
        for r in self:
            # set no exercise by default in case no exercises are allocated
            next_exercise_collection = []
            r.next_exercise_id = next_exercise_collection 
            if r.allocation_ids:
                # set to first allocated exercise by default in case no exercise assigned 
                next_exercise_collection = r.allocation_ids[0].exercise_id
                # set up exArr, which contains a list of all the allocated exercises and their allocation scores.
                exArr = []
                suitabilities = []
                exDic = dict()
                for i, allocation in enumerate(r.allocation_ids):
                    mqo_exArr = Mqo_exArr(allocation.exercise_id.id, allocation.suitability, allocation.suitability)
                    exArr.append(mqo_exArr)
                    exDic[allocation.exercise_id.id] = i
                # now adjust score if there are assignments
                if r.assignment_ids:
                    for assignment in r.assignment_ids:
                        exArr[exDic[assignment.exercise_id.id]].mod_Score(assignment)
                for s in exArr:
                    suitabilities.append(s.score)
                exID = exArr[suitabilities.index(max(suitabilities))].exercise_id
                # print("Next calculated exercise for " + str(r.name) + " is " + str(r.allocation_ids[exDic[exID]].exercise_id.name))
            # set r.next_exercise_id
            r.next_exercise_id = r.allocation_ids[exDic[exID]].exercise_id
    
    
    @api.multi
    def assignEx(self):
        print("The button worked!")
        # Create assignment id
        assignment_obj = self.env['mqo.assignment']
        for r in self:
            assignment_id = assignment_obj.create({'partner_id': r.id, 'exercise_id': r.next_exercise_id.id, 'datetime_allocated': fields.Datetime.now()})
        
