from openerp import fields, models, api

class Program(models.Model):
    _name = 'mqo.program'
    
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    individual = fields.Boolean(string="For individuals?")
    organisational = fields.Boolean(string="For organisations?")
    html = fields.Html(string="Html")

    
    brochure_attachment_id = fields.Many2one( 'ir.attachment', string='Brochure')    
    
    # brochure_attachment_ids = fields.Many2many(
    #    'ir.attachment', 'program_brochure_ir_attachments_rel',
    #    'brochure_id', 'attachment_id', string="Brochure")
                                      

class Program_brochure_attachment(models.TransientModel):
    _name = 'mqo_wizard.program_brochure'
    
    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))    
    
    program = fields.Many2one('mqo.program',
        string="Program", required=True, default=_default_program)
    name = fields.Char(string="Name")
    datas = fields.Binary(string="Brochure")
    
    @api.multi
    def attach(self):
        for program in self.program:
            # Create attachment
            # point to it
            program.attendee_ids |= self.attendee_ids
        return {}
    
    