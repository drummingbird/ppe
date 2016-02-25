# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Allocation(models.Model):
    _name = 'mqo.allocation'
    
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    suitability = fields.Float(string="Suitability rating")