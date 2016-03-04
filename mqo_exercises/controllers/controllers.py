# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.survey.controllers.main import WebsiteSurvey

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
        @http.route(['/survey/fill/<model("survey.survey"):survey>/<string:token>',
                     '/exercise/fill/<model("survey.survey"):survey>/<string:token>',
                 '/survey/fill/<model("survey.survey"):survey>/<string:token>/<string:prev>'],
                type='http', auth='public', website=True)
        def fill_survey(self, *args, **kwargs):
            return super(responseReroute, self).fill_survey(*args, **kwargs)
