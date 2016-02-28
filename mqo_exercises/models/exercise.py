# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Exercise(models.Model):
    _name = 'mqo.exercise'
    
    name = fields.Char(string="Title", required=True)
    instructions = fields.Text(string="Instructions")
    allocation_ids = fields.One2many('mqo.allocation', 'exercise_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'exercise_id', string="Assigned exercises")
    
    # Exercise params
    a.sig_m = fields.Float(string="sig_m")
    a.sig_c = fields.Float(string="sig_c")
    a.sig_r = fields.Float(string="sig_r")
    a.sig_e = fields.Float(string="sig_e")
    a.exp_m = fields.Float(string="exp_m")
    a.exp_c = fields.Float(string="exp_c")
    a.exp_r = fields.Float(string="exp_r")
    a.exp_e = fields.Float(string="exp_e")
    
    