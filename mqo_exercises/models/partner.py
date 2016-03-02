# -*- coding: utf-8 -*-
from openerp import fields, models, api
import datetime
import math

def sigmoid(t, c, r, e, down):
    return 1*down + (1 - 2*down)/(1 + math.pow(e, -(t-c)/r))

def expdec(t, c, r, e):
    return 1 - math.pow(e, -(t+c)/r)

def powinc(t, c, r, e):
    if t > c:
        return math.pow((t-c), e) / math.pow(r, e)
    else:
        return 0

class Mqo_exArr():
    exercise_id = 0
    suitability = 0
    score = 0
    
    def __init__(self, exercise_id, suitability, score):
        self.exercise_id = exercise_id
        self.suitability = suitability
        self.score = score
        self.discount = score
        self.bst = 0
        self.bur = 0
        self.tper = 0
        self.pre = 0
        self.preactived = False
 
    def mod_Score(self, assignment):
        # modify score based on an recent assignment
        elapsed_timedelta = datetime.datetime.now() - fields.Datetime.from_string(assignment.datetime_allocated)
        # elapsed_timedelta_datum = datetime.datetime.now() # - some date
        t = elapsed_timedelta.days
        a = assignment.exercise_id
        d_sig = 1 - a.sig_m*sigmoid(t, a.sig_c, a.sig_r, a.sig_e, True)
        d_exp = max(1 - a.exp_m*(1 - expdec(t, a.exp_c, a.exp_r, a.exp_e)), 0)
        self.discount = self.discount * d_sig * d_exp
        
        # need to do oldest to newest for this
        self.bur = a.bur_m*(sigmoid(t, a.bur_c, a.bur_r, a.bur_e, True) - sigmoid(t, a.bur_c2, a.bur_r, a.bur_e, True))
        print("t = " + str(t))
        print("a.bur_m = " + str(a.bur_m))
        print("a.bur_c = " + str(a.bur_c))
        print("a.bur_c2 = " + str(a.bur_c2))
        print("a.bur_r = " + str(a.bur_r))
        print("a.bur_e = " + str(a.bur_e))
        print("self.bur = " + str(self.bur))

    def mod_bst(self, bstex, assignment):
        # modify score based on an recent assignment
        elapsed_timedelta = datetime.datetime.now() - fields.Datetime.from_string(assignment.datetime_allocated)
        # elapsed_timedelta_datum = datetime.datetime.now() # - some date
        t = elapsed_timedelta.days
        bstmag = bstex.sig_m*sigmoid(t, bstex.sig_c, bstex.sig_r, bstex.sig_e, True)
        self.bst = self.bst + bstmag

    def mod_tper(self, ex):
        # modify score based on datetime
        for per in ex.tper_ids:
            currenttime = datetime.datetime.now()
            tper_start =  fields.Datetime.from_string(per.start_date)
            tper_end =  fields.Datetime.from_string(per.end_date)
            if per.annual:
                tper_start.replace(year=currenttime.year)
                tper_end.replace(year=currenttime.year)
                if (tper_end - tper_start) > 0:
                    tper_end.replace(year=currenttime.year+1)
            if currenttime >= tper_start and currenttime < tper_end: 
                self.tper = self.tper + per.mag
    
    def mod_pre(self, pre, assignment):
        # modify score based on an recent assignment
        if self.preactivated == False:
            self.pre = -10
            self.preactivated = True
        elapsed_timedelta = datetime.datetime.now() - fields.Datetime.from_string(assignment.datetime_allocated)
        # elapsed_timedelta_datum = datetime.datetime.now() # - some date
        t = elapsed_timedelta.days
        premag = pre.pow_m*powinc(t, pre.pow_c, pre.pow_r, pre.pow_e, True)
        self.pre = self.pre + premag


def getExArr(allocation_ids):
    exArr = []
    exDic = dict()
    for i, allocation in enumerate(allocation_ids):
        ex = allocation.exercise_id
        mqo_exArr = Mqo_exArr(ex.id, allocation.suitability, allocation.suitability)
        exArr.append(mqo_exArr)
        exDic[ex.id] = i
        if ex.tper_ids:
            exArr[exDic[ex.id]].mod_tper(ex)
    return exArr, exDic

def adjExArr(exArr, exDic, assignment_ids):
    for assignment in assignment_ids.sorted(key=lambda rec: rec.create_date):
        ex = assignment.exercise_id
        exArr[exDic[ex.id]].mod_Score(assignment)
        if ex.bstex_ids:
            for bstex in ex.bstex_ids:
                if bstex.boost_exercise_id.id in exDic:
                    exArr[exDic[bstex.boost_exercise_id.id]].mod_bst(bstex, assignment)
        if ex.pre_ids:
            for preex in ex.pre_ids:
                if preex.exercise_id.id in exDic:
                    exArr[exDic[preex.exercise_id.id]].mod_pre(preex, assignment)
    return exArr

def calcSuitabilities(exArr):
    suitabilities = []
    for s in exArr:
        s.score = s.discount + s.bur + s.bst + s.pre + s.tper
        suitabilities.append(s.score)
    return suitabilities

class Partner(models.Model):
    _inherit = 'res.partner'

    allocation_ids = fields.One2many('mqo.allocation', 'partner_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'partner_id', string="Assigned Exercises")
    
    next_exercise_id = fields.Many2one(comodel_name='mqo.exercise', store=True, readonly=True, compute='_compute_next_exercise', string="Next Exercise")
    
    # @api.depends('allocation_ids', 'assignment_ids')
    def _compute_next_exercise(self):
        for r in self:
            if r.allocation_ids:
                # set to first allocated exercise by default in case no exercise assigned 
                next_exercise_collection = r.allocation_ids[0].exercise_id
                # set up exArr
                exArr, exDic = getExArr(r.allocation_ids)
                # adjust score if there are assignments
                if r.assignment_ids: exArr = adjExArr(exArr, exDic, r.assignment_ids)
                suitabilities = calcSuitabilities(exArr)
                exID = exArr[suitabilities.index(max(suitabilities))].exercise_id
                print("Next calculated exercise for " + str(r.name) + " is " + str(r.allocation_ids[exDic[exID]].exercise_id.name))
                # set r.next_exercise_id
                r.next_exercise_id = r.allocation_ids[exDic[exID]].exercise_id
            else:
                r.next_exercise_id = []
    
    
    @api.multi
    def assignEx(self):
        # Create assignment id
        self._compute_next_exercise()
        assignment_obj = self.env['mqo.assignment']
        for r in self:
            assignment_id = assignment_obj.create({'partner_id': r.id, 'exercise_id': r.next_exercise_id.id, 'datetime_allocated': fields.Datetime.now()})
        
