# -*- coding: utf-8 -*-
from openerp import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'

    allocation_ids = fields.One2many('mqo.allocation', 'partner_id', string="Allocated Exercises")
    assignment_ids = fields.One2many('mqo.assignment', 'partner_id', string="Assigned Exercises")
    
    next_allocation_id = fields.Many2one(comodel_name='mqo.allocation', store=True, readonly=True, compute='_compute_next_exercise', string="Next Exercise")
    
    @api.depends('allocation_ids')
    def _compute_next_exercise(self):
        for r in self:
            next_allocation_collection = []
            if r.allocation_ids:
                next_allocation_collection = r.allocation_ids[0]
            r.next_allocation_id = next_allocation_collection