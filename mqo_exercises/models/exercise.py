# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Exercise(models.Model):
    _name = 'mqo.exercise'
    
    name = fields.Char(string="Name", required=True)
    instructions = fields.Text()