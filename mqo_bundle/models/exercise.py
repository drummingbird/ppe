from openerp import models, fields, api
import datetime

class Exercise(models.Model):
    _name = 'mqo.exercise'
    _inherit = "mqo.exercise"

    bundles = fields.Many2many('mqo.exercise', 'mqo_bundle_exericse_relation', string="Bundles")
    
