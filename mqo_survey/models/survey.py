from openerp import models, fields, api


class Question_category(models.Model):
    _name = "survey.question.category"
    _description = "Category of question category ..."

    name = fields.Char(string="Name", required=True)
  

class Mqo_question(models.Model):
    _name = 'survey.question'
    _inherit = 'survey.question'
    
    categ_id = fields.Many2one('survey.question.category', string="Category")
    
    
class Mqo_survey(models.Model):
    _name = 'survey.survey'
    _inherit = 'survey.survey'
    
    # should move survey stuff into separate module.
    group = fields.Selection(string="Group", selection=[('survey', 'Survey'), ('exercise', 'Exercise')], default='survey')


class Mqo_user_input(models.Model):
    _inherit = 'survey.user_input'

    learner = fields.Many2one('mqo.learner', 'user_input_ids', string="Learner ID")
    