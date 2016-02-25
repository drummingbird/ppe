# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Assignment(models.Model):
    _name = 'mqo.assigment'
    
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    rating = fields.Float(string="Rating")