from openerp import models, fields, api

class bundle(models.Model):
    _name = 'mqo.bundle'
    
    name = fields.Char(string="Name")
    product_templates = fields.Many2many('product.template', relation='mqo_bundle_product_relation', string="Product templates")
    exercises = fields.Many2many('mqo.exercise', relation='mqo_bundle_exericse_relation', string="Exercises")
    

