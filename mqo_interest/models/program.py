from openerp import fields, models, api

class Program_Interest(models.Model):
    _inherit = 'mqo.program'

    interest = fields.One2many('mqo.interest', 'program', string="Interest")
    
    n_interested = fields.Float(string="Number interested", compute='_n_interested')
    
    n_needed = fields.Float(string="Number needed")
      
    @api.depends('interest')
    def _n_interested(self):
        for r in self:
            if not r.interest:
                r.n_interested = 0.0
            else:
                r.n_interested = len(r.interest)

