from openerp import models, fields, api

class exercise(models.Model):
    _name = 'mqo.exercise'
    _inherit = 'mqo.exercise'
    
    bundles = fields.Many2many('mqo.bundle', relation='mqo_bundle_exercise_relation', string="Exercise bundle")

