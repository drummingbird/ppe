# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ExTimePeriod(models.Model):
    _name = 'mqo.extimeperiod'
    
    note = fields.Char(string="Note")
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    start_date = fields.Datetime(string="Start date", required=True, default=lambda self: fields.Datetime.now())
    end_date = fields.Datetime(string="End date", required=True, default=lambda self: fields.Datetime.now())
    mag = fields.Float(string="mag", default=0.0, required=True)
    annual = fields.Boolean(string="Annual?", default=False)

class ExBoosted(models.Model):
    _name = 'mqo.exboosted'
    
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    boost_exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    sig_m = fields.Float(string="sig_m", default=0.0)
    sig_c = fields.Float(string="sig_c", default=0.0)
    sig_r = fields.Float(string="sig_r", default=1.0)
    sig_e = fields.Float(string="sig_e", default=1.0)

class ExPre(models.Model):
    _name = 'mqo.expre'
    
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    pre_exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    pow_m = fields.Float(string="pow_m", default=10.0)
    pow_c = fields.Float(string="pow_c", default=0.0)
    pow_r = fields.Float(string="pow_r", default=1.0)
    pow_e = fields.Float(string="pow_e", default=1.0)


class Exercise(models.Model):
    _name = 'mqo.exercise'
    
    name = fields.Char(string="Title", required=True)
    instructions = fields.Text(string="Instructions")
    allocation_ids = fields.One2many('mqo.allocation', 'exercise_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'exercise_id', string="Assigned exercises")
    
    # Exercise params
    sig_m = fields.Float(string="sig_m", default=0.0)
    sig_c = fields.Float(string="sig_c", default=0.0)
    sig_r = fields.Float(string="sig_r", default=1.0)
    sig_e = fields.Float(string="sig_e", default=1.0)
    exp_m = fields.Float(string="exp_m", default=0.0)
    exp_c = fields.Float(string="exp_c", default=0.0)
    exp_r = fields.Float(string="exp_r", default=1.0)
    exp_e = fields.Float(string="exp_e", default=1.0)
    bur_m = fields.Float(string="bur_m", default=0.0)
    bur_c = fields.Float(string="bur_c", default=0.0)
    bur_r = fields.Float(string="bur_r", default=1.0)
    bur_e = fields.Float(string="bur_e", default=1.0)
    bur_c2 = fields.Float(string="bur_c2", default=0.0)
    bst_m = fields.Float(string="bst_m", default=0.0)
    dur = fields.Float(string="dur", default=1.0)
    tper_ids = fields.One2many('mqo.extimeperiod', 'exercise_id', string="Time periods")
    bstex_ids = fields.One2many('mqo.exboosted', 'exercise_id', string="Boosted exercises")
    pre_ids = fields.One2many('mqo.expre', 'pre_exercise_id', string="Prerequisite for")
    
    surveyq_dat =  fields.One2many('mqo.exsurveyqdata', 'exercise_id', string="Survey question data")
    
class ExSurveyQCoef(models.Model):
    _name = 'mqo.exsurveyqcoef'
    
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    survey_question = fields.Many2one('survey.question',
        ondelete='cascade', string="Exercise", required=True)
    coef = fields.Float(string="Coefficient", default=0.0)

