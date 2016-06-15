from openerp import fields, models, api

class Program(models.Model):
    _name = 'mqo.program'

    #api.multi
    def _get_binary_filesystem(self):
        """ Display the binary from ir.attachment, if already exist """
        res = {}
        attachment_obj = self.env['ir.attachment']
    
        for record in self:
            res[record.id] = False
            attachment_ids = attachment_obj.search([('res_model','=',self._name),('res_id','=',record.id)])
            if attachment_ids:
                record.brochure = attachment_ids[0].datas
    
    #api.multi
    def _set_binary_filesystem(self):
        """ Create or update the binary in ir.attachment when we save the record """
        attachment_obj = self.env['ir.attachment']
        
        for record in self:
            attachment_ids = attachment_obj.search([('res_model','=',self._name),('res_id','=',record.id)])
            if record.brochure:
                if attachment_ids:
                    attachment_ids[0].write({'datas': record.brochure})
                else:
                    attachment_obj.create({'res_model': self._name, 'res_id': record.id, 'name': '/program/equip/brochure.pdf', 
                                           'url': '/program/equip/brochure.pdf', 'datas': record.brochure, 
                                           'datas_fname': 'brochure.pdf', 'store_fname': 'brochure.pdf'})
            else:
                attachment_ids[0].unlink()

    
    name = fields.Char(string="Name")
    
    description = fields.Text(string="Description")

    individual = fields.Boolean(string="For individuals?")
    organisational = fields.Boolean(string="For organisations?")
    brochure = fields.Binary(compute=_get_binary_filesystem, inverse=_set_binary_filesystem, string='Brochure', store=False)
