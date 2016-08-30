# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime

class Allocation(models.Model):
    _name = 'mqo.allocation'
    
    learner = fields.Many2one('mqo.learner', string="Learner", required=True)
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    suitability = fields.Float(string="Suitability rating", compute="_compute_suitability", store=True)
    
    @api.depends('learner', 'exercise_id')
    def _compute_suitability(self):
        suitability = 1    
        self.suitability = suitability