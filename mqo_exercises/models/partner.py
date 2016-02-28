# -*- coding: utf-8 -*-
from openerp import fields, models, api
from datetime import datetime, timedelta

def sigmoid(time, basetime, rate, down):
    return 1*down + (1 - 2*down)/(1+math.exp(-(time-basetime)/rate))

class Mqo_exArr():
    exercise_id = 0
    suitability = 0
    score = 0
    
    def __init__(self, exercise_id, suitability, score):
        self.exercise_id = exercise_id
        self.suitability = suitability
        self.score = score
# 
    # def mod_Score(self, assignment):
        # modify score based on an recent assignment
    #    elapsed_timedelta = datetime.datetime.now() - assignment.datetime_allocated
        # elapsed_timedelta_datum = datetime.datetime.now() # - some date
    #    t = elapsed_timedelta.days
    #    a = assignment.exercise_id
    #    dWait = a.waitmag*sigmoid(t, a.waittime, a.waitrate, False)
        # dBurst, dBoost, dCyclic
    #    self.score = self.score - dWait


class Partner(models.Model):
    _inherit = 'res.partner'

    allocation_ids = fields.One2many('mqo.allocation', 'partner_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'partner_id', string="Assigned Exercises")
    
    next_exercise_id = fields.Many2one(comodel_name='mqo.exercise', store=True, readonly=True, compute='_compute_next_exercise', string="Next Exercise")
    
    @api.depends('allocation_ids')
    def _compute_next_exercise(self):
        for r in self:
            # set no exercise by default in case no exercises are allocated
            next_exercise_collection = [] 
            if r.allocation_ids:
                # set to first allocated exercise by default in case no exercise assigned 
                next_exercise_collection = r.allocation_ids[0].exercise_id
                # set up exArr, which contains a list of all the allocated exercises and their allocation scores.
                # exArr = []
                # suitabilities = []
                # exDic = dict()
                # for i, allocation in enumerate(r.allocation_ids):
                #    mqo_exArr = Mqo_exArr(allocation.exercise_id.id, allocation.suitability, allocation.suitability)
                #    exArr.append(mqo_exArr)
                #    suitabilities.append(allocation.suitability)
                #    exDic[allocation.exercise_id.id] = i
                #maxSuitability = max(suitabilities)
                # now adjust score
                #for assignment in r.assignment_ids:
                #    exArr[exDic[allocation.exercise_id.id]].mod_Score(assignment)
            # set r.next_exercise_id
            r.next_exercise_id = next_exercise_collection
            
