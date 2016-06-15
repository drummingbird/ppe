from openerp import fields, models, api

class Interest(models.Model):
    _name = 'mqo.interest'

    name = fields.Char(string="Contact name")
    contact_org = fields.Char(string="Contact organisation")
    contact_email = fields.Char(string="Contact email")
    contact_phone = fields.Char(string="Contact phone")
    
    program = fields.Many2one('mqo.program', ondelete='cascade', string="Program", required=True)
  
    
    date_registered = fields.Date(string="Date", default=fields.Date.context_today)
    
    timeframe =  fields.Selection([('1', 'Within 3 months'),
                               ('2', 'Within 6 months'),
                               ('3', 'Within 12 months')],
                               string='Timeframe', readonly=True)
    
    private_course = fields.Boolean(string="Private course")
    
    location = fields.Selection([('auckland', 'Auckland'),
                               ('wellington', 'Wellington'),
                               ('christchurch', 'Christchurch')],
                               string='Location', readonly=True)
    
    message = fields.Text(string="Message / Comments")
    extra_info = fields.Text(string="Extra info")