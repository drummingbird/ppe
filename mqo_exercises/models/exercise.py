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

class ExBoosted(models.Model):
    _name = 'mqo.exboosted'
    
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    boost_exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    mag = fields.Float(string="mag", default=0.0)
    duration = fields.Float(string="duration", default=0.0)


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
    sig_e = fields.Float(string="sig_e", default=0.0)
    exp_m = fields.Float(string="exp_m", default=0.0)
    exp_c = fields.Float(string="exp_c", default=0.0)
    exp_r = fields.Float(string="exp_r", default=1.0)
    exp_e = fields.Float(string="exp_e", default=0.0)
    bur_m = fields.Float(string="bur_m", default=0.0)
    bur_c = fields.Float(string="bur_c", default=0.0)
    bur_r = fields.Float(string="bur_r", default=1.0)
    bur_e = fields.Float(string="bur_e", default=0.0)
    bur_c2 = fields.Float(string="bur_c2", default=0.0)
    bst_m = fields.Float(string="bst_m", default=0.0)
    dur = fields.Float(string="dur", default=1.0)
    tper = fields.One2many('mqo.extimeperiod', 'exercise_id', string="Time periods")
    bstex = fields.One2many('mqo.exboosted', 'exercise_id', string="Boosted exercises")