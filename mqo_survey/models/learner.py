from openerp import fields, models, api

class Learner_strengths(models.Model):
    _inherit = 'mqo.learner'
    
    user_input_ids = fields.One2many('survey.user_input', 'learner', string="User input IDs")