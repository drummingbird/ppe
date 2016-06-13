from openerp import fields, models, api

class Program_Interest(models.Model):
    _inherit = 'res.program'

    interest = fields.One2many('mqo.interest', 'program', string="Program")
