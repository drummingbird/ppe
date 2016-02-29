# -*- coding: utf-8 -*-
from openerp import models, fields, api

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
    
    