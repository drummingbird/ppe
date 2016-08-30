from openerp import fields, models, api

class Users(models.Model):
    _inherit = 'res.users'

    learner = fields.One2many('mqo.learner', 'user', string="Learner ID")
