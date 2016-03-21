from openerp import models, fields, api
import datetime

class bundle(models.Model):
    _name = 'mqo.bundle'
    
    name = fields.Char(string="Name")
    product_templates = fields.Many2many('product.template', relation='mqo_bundle_product_relation', string="Product templates")
    exercises = fields.Many2many('mqo.exercise', relation='mqo_bundle_exericse_relation', string="Exercises")


class bundle_allocation(models.Model):
    _name = 'mqo.bundle.allocation'
    
    bundle = fields.Many2one('mqo.bundle', string="Exercise bundle")
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    expiry_datetime = fields.Datetime(string="Expiry", default=lambda self: fields.Datetime.to_string(datetime.datetime.now() + datetime.timedelta(days=365)))
    
    @api.multi
    def _check_expiry(self):
        # Automatically raise warning when approaching expiry, and delete expired bundle allocations.
        warning_list_ids = []
        for r in self:
            current_datetime = datetime.datetime.now() 
            if current_datetime > r.expiry_datetime:
                r.unlink()
            elif current_datetime > r.expiry_datetime - datetime.timedelta(days=21):
                warning_list_ids.append(r.id)
        return warning_list_ids
