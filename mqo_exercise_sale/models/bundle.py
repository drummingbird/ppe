from openerp import models, fields, api
import datetime

class Bundle(models.Model):
    _name = 'mqo.bundle'
    _inherit = "mqo.bundle"

    product_templates = fields.Many2many('product.template', 'mqo_bundle_product_relation', 'bundle_id', 'product_template_id', string="Product templates")


