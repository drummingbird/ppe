# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.survey.controllers.main import WebsiteSurvey
import json
import logging

class MyLearning(http.Controller):
    @http.route('/mylearning/mylearning/', type='http', auth='public', website=True)
    def index(self, **kw):
        # Partners = http.request.env['res.partner']
        partner = request.env['res.users'].browse(request.uid).partner_id
        if partner:
            ResPartner = request.env['res.partner'].browse(partner.id)
            currentex = ResPartner.next_exercise_id
            return request.render('mqo_exercises.index', {
                'exercises': currentex
            })
        else:
            return request.render('mqo_exercises.index', {'exercises': []})

        
class ExerciseResponse(http.Controller):
    
    def _check_bad_cases(self, cr, uid, request, assignment, assignment_obj, token, context=None):
        # In case of bad survey, redirect to surveys list
        if assignment_obj.exists(cr, SUPERUSER_ID, assignment.id, context=context) == []:
            print('assignment not found')
            return request.website.render("website.403")

        # redirect if token is invalid.
        if assignment.response_token != token:
            print('response token was invalid')
            return request.website.render("website.403")

        # In case of auth required, block public user
        if uid == request.website.user_id.id:
            print('authorisation required')
            return request.website.render("survey.auth_required", {'survey': assignment.response_survey})
        
        # no surveys assigned
        if not assignment.response_survey:
            print('assignment has no response surveys')
            return request.website.render("website.403")

        # Everything seems to be ok
        return None
    
# Survey wrapper for starting a response
    @http.route(['/exercise/response/<model("mqo.assignment"):assignment>/<string:token>'],
                type='http', auth='public', website=True)
    def survey_wrapper(self, assignment, token, prev=None, **post):
        '''wraps a response'''
        cr, uid, context = request.cr, request.uid, request.context
        assignment_obj = request.registry['mqo.assignment']
        survey_obj = request.registry['survey.survey']
        user_input_obj = request.registry['survey.user_input']

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(cr, uid, request, assignment, assignment_obj, token, context=context)
        if errpage:
            return errpage


        # see if response for this assignment already exists, and create one for this assignment if needed.
        try:
            user_input_id = user_input_obj.search(cr, SUPERUSER_ID, [('token', '=', assignment.response_token)], context=context)[0]
        except IndexError:  # No response currently exists for this assignment
            vals = {'survey_id': assignment.response_survey.id, 'partner_id': assignment.partner_id.id, 'token': assignment.response_token, 'state': 'skip'}
            user_input_id = user_input_obj.create(cr, uid, vals, context=context)
            user_input = user_input_obj.browse(cr, uid, [user_input_id], context=context)[0]
            # record response in assignment
            assignment.write({'responses': user_input_id}) 
        else:
            user_input = user_input_obj.browse(cr, SUPERUSER_ID, [user_input_id], context=context)[0]

        return request.redirect('/exercise/fill/%s/%s' % (assignment.response_survey.id, user_input.token))
    
class responseReroute(WebsiteSurvey):
    @http.route(['/exercise/fill/<model("survey.survey"):survey>/<string:token>'],
            type='http', auth='public', website=True)
    def fill_exercise(self, *args, **kwargs):
        return super(responseReroute, self).fill_survey(*args, **kwargs)
    
    # AJAX submission of a page
    @http.route(['/survey/submit/<model("survey.survey"):survey>'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit(self, survey, **post):
        _logger.debug('Incoming data: %s', post)
        page_id = int(post['page_id'])
        cr, uid, context = request.cr, request.uid, request.context
        survey_obj = request.registry['survey.survey']
        questions_obj = request.registry['survey.question']
        questions_ids = questions_obj.search(cr, uid, [('page_id', '=', page_id)], context=context)
        questions = questions_obj.browse(cr, uid, questions_ids, context=context)

        # Answer validation
        errors = {}
        for question in questions:
            answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
            errors.update(questions_obj.validate_question(cr, uid, question, post, answer_tag, context=context))

        ret = {}
        if (len(errors) != 0):
            # Return errors messages to webpage
            ret['errors'] = errors
        else:
            # Store answers into database
            user_input_obj = request.registry['survey.user_input']

            user_input_line_obj = request.registry['survey.user_input_line']
            try:
                user_input_id = user_input_obj.search(cr, SUPERUSER_ID, [('token', '=', post['token'])], context=context)[0]
            except KeyError:  # Invalid token
                return request.website.render("website.403")
            user_input = user_input_obj.browse(cr, SUPERUSER_ID, user_input_id, context=context)
            user_id = uid if user_input.type != 'link' else SUPERUSER_ID
            for question in questions:
                answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
                user_input_line_obj.save_lines(cr, user_id, user_input_id, question, post, answer_tag, context=context)

            go_back = post['button_submit'] == 'previous'
            next_page, _, last = survey_obj.next_page(cr, uid, user_input, page_id, go_back=go_back, context=context)
            vals = {'last_displayed_page_id': page_id}
            if next_page is None and not go_back:
                vals.update({'state': 'done'})
            else:
                vals.update({'state': 'skip'})
            user_input_obj.write(cr, user_id, user_input_id, vals, context=context)
            ret['redirect'] = '/exercise/fill/%s/%s' % (survey.id, post['token'])
            if go_back:
                ret['redirect'] += '/prev'
        return json.dumps(ret)
