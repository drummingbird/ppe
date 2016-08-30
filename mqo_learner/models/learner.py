from openerp import fields, models, api

class Learner(models.Model):
    _name = 'mqo.learner'
    
    name = fields.Char(string="Name")
    user = fields.Many2one('res.users', string="User ID")
    
    @api.one
    @api.constrains('user')
    def _check_user(self):
        if len(self.user) > 1:
            raise ValidationError("A learner can be matched to only one partner.")