# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime, timedelta

class Assignment(models.Model):
    _name = 'mqo.assignment'
    
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    rating = fields.Float(string="Rating")
    datetime_allocated = fields.DateTime(string="Date Time Stamp")