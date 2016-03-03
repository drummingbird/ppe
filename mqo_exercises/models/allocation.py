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
        at_least_one_response = False
        
        if self.exercise_id.surveyq_dat:
            user_input_ids = []
            response_meta_recordset = self.env['survey.user_input'].search([('partner_id', '=', self.partner_id.id)])
            for record in response_meta_recordset:
                user_input_ids.append(record.id)
            
            print('user_input_ids=' + str(user_input_ids))
            if user_input_ids:
                for exsurveyqcoef in self.exercise_id.surveyq_dat:
                    question = exsurveyqcoef.survey_question
                    question_response = self.env['survey.user_input_line'].search([('question_id', '=', question.id),
                                                                                   ('user_input_id', 'in', user_input_ids)],
                                                                                   order='date_create desc', limit=1)
                    if question_response and not at_least_one_response: 
                        suitability = 0
                        at_least_one_response = True
                        print('at least one response found')
                    if at_least_one_response:
                        print('response.value=' + str(question_response.value_number))
                        print('exsurveyqcoef.coef=' + str(exsurveyqcoef.coef))
                        suitability = suitability + float(question_response.value_number)*exsurveyqcoef.coef
        
        self.suitability = suitability