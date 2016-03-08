from openerp import models, fields, api
import datetime

class sale_order(model.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(sale_order, self).action_confirm()
        for order in self:
            hasbundles, so_id = any(product.bundles for product in order.order_line.product_id), order.id
            order.order_line._allocate_exercises(order.partner_id, confirm=True)
        return res


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _allocate_exercises(self, partner, confirm=True):
        """ Create or update exercise allocations linked to a invoice line. An invoice line
        has a quantity attribute that will be the number of
        years subscription linked to this line. """

        allocation_obj = self.env['mqo.allocation']
        
        for line in [l for l in self if l.product_id.bundles]:
            for bundle in line.product_id.bundles:
                for exercise in bundle.exercises:
                    # see if allocation already exists, and update or create one if needed.
                    try:
                        allocation_id = allocation_obj.search({'partner_id': partner.id, 'exercise_id': exercise.id})[0]
                    except IndexError:  # No response currently exists for this assignment
                        expiry_datetime = fields.Datetime.to_string(datetime.datetime.now() + datetime.timedelta(days=365*line.quantity)) 
                        allocation_id = allocation_obj.create({'partner_id': partner.id, 'exercise_id': exercise.id, 'expiry_datetime': expiry_datetime})
                    else:
                        expiry_datetime = fields.Datetime.to_string(fields.Datetime.from_string(allocation_id.expiry_datetime) + datetime.timedelta(days=365*line.quantity))
                        allocation_id.write({'expiry_datetime': expiry_datetime})
        return True
