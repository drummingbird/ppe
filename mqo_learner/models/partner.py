from openerp import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'

    learner = fields.One2many('mqo.learner', 'partner', string="Learner ID")
