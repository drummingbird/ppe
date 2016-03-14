# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.survey.controllers.main import WebsiteSurvey
import json
import logging

_logger = logging.getLogger(__name__)

        
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
        
        print('survey_id ' + str(survey_id))
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

        # Define dictionary to interpret results: question_id -- category
        ir_model_data = request.registry['ir.model.data']
        
        dic_ids = dict()
        for page in survey.page_ids:
            for question in page.question_ids:
                ir_model_id = ir_model_data.search(cr, uid, [('module', '=', 'survey'), ('res_id', '=', question.id)], context=context)[0]
                dat = ir_model_data.browse(cr, uid, [ir_model_id], context=context)[0]
                dic_ids[question.id] = dat.name
        
        print(dic_ids)
        # Identify what category each question is in
        dic_cat = dic_ids
        # strengths questions are named X_X_X_{strengthname}_X 
        for item, value in dic_cat.iteritems():
                dic_cat[item] = value.split('_')[3]
        
        print(dic_cat)
        # create result dictionary including each unique category
        categories = set(dic_cat.values())
        res = dict()
        for item in categories:
            res[item] = 0
        
        print(res)
        # get responses
        user_input_line_obj = request.registry['survey.user_input_line']
        user_input_line_ids = user_input_line_obj.search(cr, SUPERUSER_ID, [('survey_id', '=', survey_id)], context=context)
        user_input_line = user_input_line_obj.browse(cr, SUPERUSER_ID, [user_input_line_ids], context=context)
        
        # analyze survey results, using dictionary of question ids and categories 
        for line in user_input_line:
            cat = dic_cat[line.question_id]
            res[cat] = res[cat] + line.quizz_mark
        
        res_sorted = []  
        # Sort through strengths in order
        for key, value in sorted(t.iteritems(), key=lambda (k,v): (v,k),reverse=True):  
            diction= {"value": value, "name": key}  
            res_sorted.append(diction)

        vals = {'strengths': res_sorted}
        print(vals)
        return request.website.render("mqo_strengths.results", vals)    
            
        
