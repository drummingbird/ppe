# -*- coding: utf-8 -*-
from openerp import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'

    allocation_ids = fields.One2many('mqo.allocation', 'partner_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'partner_id', string="Assigned Exercises")
    
    next_exercise_id = fields.Many2one(comodel_name='mqo.allocation', store=True, readonly=True, compute='_compute_next_allocation')
    
    @api.depends('allocation_ids')
    def _compute_next_allocation(self):
        for r in self:
            next_allocation_collection = []
            if r.allocation_ids:
                next_allocation_collection.append(r.allocation_ids[0])
            r.next_exercise_id = next_allocation_collection