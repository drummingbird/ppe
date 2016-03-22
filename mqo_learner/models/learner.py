from openerp import fields, models, api

class Learner(models.Model):
    _name = 'mqo.learner'
    
    name = fields.Char(string="Name")
    partner = fields.Many2one('res.partner', string="Partner ID")
    
    @api.one
    @api.constrains('partner')
    def _check_partner(self):
        if len(self.partner) > 1:
            raise ValidationError("A learner can be matched to only one partner.")