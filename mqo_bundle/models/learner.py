from openerp import models, fields, api
import datetime

class Bundle(models.Model):
    _name = 'mqo.bundle'
    _inherit = "mqo.bundle"

    bundle_allocations = fields.One2many('mqo.bundle.allocation', 'learner', string="Allocated exercise bundles")