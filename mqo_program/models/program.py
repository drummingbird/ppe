from openerp import fields, models, api

class Program(models.Model):
    _name = 'mqo.program'
    
    name = fields.Char(string="Name")
