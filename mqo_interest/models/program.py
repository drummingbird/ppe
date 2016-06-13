from openerp import fields, models, api

class Program_Interest(models.Model):
    _inherit = 'mqo.program'

    interest = fields.One2many('mqo.interest', 'program', string="Program")
