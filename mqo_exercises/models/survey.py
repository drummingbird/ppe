from openerp import models, fields, api

class Mqo_survey(models.Model):
    _name = 'survey.survey'
    _inherit = 'survey.survey'
    
    group = fields.Selection(string="Group", selection=[('survey', 'Survey'), ('exercise', 'Exercise')], default='survey')
