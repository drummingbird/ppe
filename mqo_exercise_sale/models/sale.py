from openerp import models, fields, api
import datetime

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_allocate_bundles(self):
        print("Allocate bundles action has been triggered.")
        for order in self:
            hasbundles, so_id = any(product.bundles for product in order.order_line.product_id), order.id
            order.order_line._allocate_bundles(order.partner_id, confirm=True)
        return True


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _allocate_bundles(self, partner, confirm=True):
        """ Create or update bundle allocations linked to a invoice line. An invoice line
        has a quantity attribute that will be the number of
        years subscription linked to this line. """

        print('Allocating bundles')
        # get list of all current bundle allocations for partner_id
        bundle_allocation_obj = self.env['mqo.bundle.allocation']
        bundle_allocations = bundle_allocation_obj.search([('partner_id', '=', partner.id)])
        bundle_id_list = []
        for bundle_allocation in bundle_allocations:
            bundle_id_list.append(bundle_allocation.bundle.id)
        
        for line in [l for l in self if l.product_id.bundles]:
            for bundle in line.product_id.bundles:
                # Allocate bundles, or boost their expiry date.
                if bundle.id in bundle_id_list:
                    index = bundle_id_list.index(bundle.id)
                    oldExpiry = fields.Datetime.from_string(bundle_allocations[index].expiry_datetime)
                    expiry_datetime = fields.Datetime.to_string(oldExpiry + datetime.timedelta(days=365*line.product_uom_qty))
                    bundle_allocations[index].write({'expiry_datetime': expiry_datetime})
                    print('Allocated new bundle')
                else:
                    expiry_datetime = fields.Datetime.to_string(datetime.datetime.now() + datetime.timedelta(days=365*line.product_uom_qty))
                    bundle_allocation_id = bundle_allocation_obj.create({'bundle': bundle.id, 'partner_id': partner.id, 'expiry_datetime': expiry_datetime})
                    print('Increased bundle expiry date')
        return True
