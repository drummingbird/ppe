# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.survey.controllers.main import WebsiteSurvey
import json
import logging

_logger = logging.getLogger(__name__)


class StrengthItem():
    name = ''
    value = 0
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
 

        
class StrengthsResults(http.Controller):
    
    def _check_bad_cases(self, cr, uid, request, survey_obj, survey, user_input_obj, context=None):
        # In case of bad survey, redirect to surveys list
        if survey_obj.exists(cr, SUPERUSER_ID, survey.id, context=context) == []:
            return werkzeug.utils.redirect("/survey/")

        # In case of auth required, block public user
        if survey.auth_required and uid == request.website.user_id.id:
            return request.website.render("survey.auth_required", {'survey': survey})

        # In case of non open surveys
        if survey.stage_id.closed:
            return request.website.render("survey.notopen")

        # If there is no pages
        if not survey.page_ids:
            return request.website.render("survey.nopages")

        # Everything seems to be ok
        return None

# Survey wrapper for strengths survey response
    @http.route(['/mystrengths/<string:token>'],
                type='http', auth='public', website=True)
    def survey_wrapper(self, token, prev=None, **post):
        '''wraps a response'''
        cr, uid, context = request.cr, request.uid, request.context
        survey_obj = request.registry['survey.survey']
        user_input_obj = request.registry['survey.user_input']

        survey_id = survey_obj.search(cr, SUPERUSER_ID, [('title', '=', 'Strengths')], context=context)[0]
        survey = survey_obj.browse(cr, SUPERUSER_ID, [survey_id], context=context)[0]
        
        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(cr, uid, request, survey_obj, survey, user_input_obj, context=context)
        if errpage:
            return errpage

        # see if response for this survey already exists.
        try:
            user_input_id = user_input_obj.search(cr, SUPERUSER_ID, [('token', '=', token), ('survey_id', '=', survey_id)], context=context)[0]
        except IndexError:  # No response currently exists for this assignment
            print('response token was invalid')
            return request.website.render("website.403")
        else:
            user_input = user_input_obj.browse(cr, SUPERUSER_ID, [user_input_id], context=context)[0]

        # Identify what category each question is in
        dic_cat = dict()
        for page in survey.page_ids:
            question_ids = []
            for question in page.question_ids:
                question_ids.append(question.id) 
                dic_cat[question.id] = question.categ_id.name

        # create result dictionary including each unique category
        strength_names = set(dic_cat.values())
        res = dict()
        for item in strength_names:
            res[item] = 0.0
        
        n = res
        
        # get responses
        #user_input_line_obj = request.registry['survey.user_input_line']
        #user_input_line_ids = user_input_line_obj.search(cr, SUPERUSER_ID, [('survey_id', '=', survey_id)], context=context)
        #user_input_line = user_input_line_obj.browse(cr, SUPERUSER_ID, user_input_line_ids, context=context)
        
        # analyze survey results, using dictionary of question ids and strength_names 
        #for line in user_input_line:
        for line in user_input.user_input_line_ids:
            cat = dic_cat[line.question_id.id]
            res[cat] = (res[cat]*(n[cat]) + line.quizz_mark) / (n[cat] + 1.0)  
            n[cat] = n[cat] + 1.0
        
        strengths_obj = request.registry['mqo.snippet.strengths']
        # strength_ids = strengths_obj.search(cr, SUPERUSER_ID, [], context=context)
        # strengths = strengths_obj.browse(cr, SUPERUSER_ID, strength_ids, context=context)
        strengths = strengths_obj.search_read(cr, SUPERUSER_ID, [], ['id', 'name', 'title', 'text'])
        for strength in strengths:
            strength["value"] = res[strength["name"]]
     
        strengths = strengths.sorted(key=lambda strength: strength["value"], reverse=True)
        for i, strength in enumerate(strengths):
            strength["seq_num"] = i + 1
        
        vals = {'strengths': strengths}
        return request.website.render("mqo_strengths.results", vals)    
            
        
