from openerp import fields, models, api

class Program(models.Model):
    _name = 'mqo.program'

    #api.multi
    def _get_binary_brochure(self):
        """ Display the binary from ir.attachment, if already exist """
        res = {}
        attachment_obj = self.env['ir.attachment']
    
        for record in self:
            res[record.id] = False
            name = '/program/' + record.name.lower() + '/brochure.pdf'
            attachment_ids = attachment_obj.search([('res_model','=',self._name),('res_id','=',record.id), ('name', '=', name)])
            if attachment_ids:
                record.brochure = attachment_ids[0].datas
    
    #api.multi
    def _set_binary_brochure(self):
        """ Create or update the binary in ir.attachment when we save the record """
        attachment_obj = self.env['ir.attachment']
        
        for record in self:
            name = '/program/' + record.name.lower() + '/brochure.pdf'
            attachment_ids = attachment_obj.search([('res_model','=',self._name),('res_id','=',record.id), ('name', '=', name)])
            if record.brochure:
                if attachment_ids:
                    attachment_ids[0].write({'datas': record.brochure})
                else:
                    attachment_obj.create({'res_model': self._name, 'res_id': record.id, 'name': name, 
                                           'url': name, 'datas': record.brochure, 
                                           'datas_fname': 'brochure.pdf', 'store_fname': 'brochure.pdf'})
            else:
                attachment_ids[0].unlink()

    #api.multi
    def _get_binary_image(self):
        """ Display the binary from ir.attachment, if already exist """
        res = {}
        attachment_obj = self.env['ir.attachment']
    
        for record in self:
            res[record.id] = False
            name = '/program/' + record.name.lower() + '/image.jpg'
            attachment_ids = attachment_obj.search([('res_model','=',self._name),('res_id','=',record.id), ('name', '=', name)])
            if attachment_ids:
                record.image = attachment_ids[0].datas
    
    #api.multi
    def _set_binary_image(self):
        """ Create or update the binary in ir.attachment when we save the record """
        attachment_obj = self.env['ir.attachment']
        
        for record in self:
            name = '/program/' + record.name.lower() + '/image.jpg'
            attachment_ids = attachment_obj.search([('res_model','=',self._name),('res_id','=',record.id), ('name', '=', name)])
            if record.image:
                if attachment_ids:
                    attachment_ids[0].write({'datas': record.image})
                else:
                    attachment_obj.create({'res_model': self._name, 'res_id': record.id, 'name': name, 
                                           'url': name, 'datas': record.image, 
                                           'datas_fname': 'image.jpg', 'store_fname': 'image.jpg'})
            else:
                attachment_ids[0].unlink()

    
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    
    session_detail = fields.Char(string="Session details")
    timeframe_detail = fields.Char(string="Timeframe")

    individual = fields.Boolean(string="For individuals?")
    organisational = fields.Boolean(string="For organisations?")
    pagelink = fields.Char(string="Pagelink")
    brochure = fields.Binary(compute=_get_binary_brochure, inverse=_set_binary_brochure, string='Brochure', store=False)
    image = fields.Binary(compute=_get_binary_image, inverse=_set_binary_image, string='Image', store=False)
    benefits = fields.One2many('mqo.benefit_program_link', 'program', string="Benefits")
   