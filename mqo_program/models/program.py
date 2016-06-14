from openerp import fields, models, api

class Program(models.Model):
    _name = 'mqo.program'
    
    name = fields.Char(string="Name")
    
    description = fields.Text(string="Description")

    individual = fields.Boolean(string="For individuals?")
    organisational = fields.Boolean(string="For organisations?")