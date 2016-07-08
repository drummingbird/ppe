from openerp import models, fields, api

class Mqo_strengths_question_category(models.Model):
    _name = "survey.question.category"
    _description = "Category of question category ..."

    name = fields.Char(string="Name", required=True)
  
class Mqo_strengths_question(models.Model):
    _name = 'survey.question'
    _inherit = 'survey.question'
    
    categ_id = fields.Many2one('survey.question.category', string="Category")