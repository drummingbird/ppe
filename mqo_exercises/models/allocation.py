# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Allocation(models.Model):
    _name = 'mqo.allocation'
    
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    suitability = fields.Float(string="Suitability rating", compute="_compute_suitability", store=True)
    
    @api.depends('partner_id', 'exercise_id')
    def _compute_suitability(self):
        suitability = 1
        at_least_one_resonse = False
        
        if self.exercise_id.surveyq_dat:
            user_input_ids = []
            response_meta_recordset = self.env['survey.user_input'].search([('partner_id', '=', self.partner_id.id)])
            for record in response_meta_recordset:
                user_input_ids.append(record.id)
            
            if user_input_ids:
                for exsurveyqcoef in self.exercise_id.surveyq_dat:
                    question = exsurveyqcoef.survey_question
                    question_response = self.env['survey.user_input_line'].search([('question_id', '=', question.id),
                                                                                   ('user_input_id', 'in', user_input_ids)],
                                                                                   order='date_create desc', limit=1)
                    if question_response: 
                        suitability = 0
                        at_least_one_resonse = True
                    if at_least_one_resonse:
                        suitability = suitability + float(question_response.value_number)*exsurveyqcoef.coef
        
        self.suitability = suitability