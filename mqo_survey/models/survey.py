from openerp import models, fields, api

class Mqo_question(models.Model):
    _name = 'survey.question'
    _inherit = 'survey.question'
    
    review_text = fields.Char(string="Review text")
    
class Mqo_survey(models.Model):
    _name = 'survey.survey'
    _inherit = 'survey.survey'
    
    # should move survey stuff into separate module.
    group = fields.Selection(string="Group", selection=[('survey', 'Survey'), ('exercise', 'Exercise')], default='survey')


class Mqo_user_input(models.Model):
    _inherit = 'survey.user_input'

    learner = fields.Many2one('mqo.learner', string="Learner ID")
    