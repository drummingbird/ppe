# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    allocation_id = fields.One2many('mqo.allocation', 'partner_id', string="Allocated Exercises")
    assignment_id = fields.One2many('mqo.assignment', 'partner_id', string="Assigned Exercises")