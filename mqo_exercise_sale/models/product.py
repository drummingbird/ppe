from openerp import models, fields, api

class product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    
    hasbundles = fields.Boolean(string="Is an MQO exercise product?")
    bundles = fields.Many2many('mqo.bundle', relation='mqo_bundle_product_relation', string="Exercise bundle")

