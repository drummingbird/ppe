# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.survey.controllers.main import WebsiteSurvey
import json
import logging

_logger = logging.getLogger(__name__)

class MyLearning(http.Controller):
    @http.route('/mylearning/mylearning/', type='http', auth='public', website=True)
    def index(self, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        user = request.registry['res.users'].browse(cr, uid, uid, context=context)
        learner = user.learner
        if learner:
            currentex = learner.next_exercise_id
            assignments = learner.assignments
            responses = False
            return request.render('mqo_exercises.index', {
                'exercises': currentex,
                'assignments': assignments,
                'responses': responses
            })
        else:
            return request.render('mqo_exercises.index', {'exercises': []})

        
class ExerciseResponse(http.Controller):
    # AJAX submission of a page
    @http.route(['/assignment/rating'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit(self, **post):
        _logger.debug('Incoming data: %s', post)
        ret = {}
        
        if post['assignment_id']:
            cr, uid, context = request.cr, request.uid, request.context
            assignment = request.env['mqo.assignment'].browse(int(post['assignment_id']))[0]
            if assignment:
                print('assignment should follow: ')
                print(assignment.learner.name)
                learner = request.env['mqo.learner'].browse(assignment.learner.id)
                
                if post['rating']:
                    assignment.write({'rating': post['rating']})
                    learner.assignEx()
                    newAssignment = learner.assignments[0]
                    newExercise = newAssignment.exercise_id 
                    ret['reply'] = {
                                       'assignment_id': newAssignment.id,
                                       'exercise_id': newExercise.id,
                                       'exercise_name': newExercise.name,
                                       'exercise_instructions': newExercise.instructions
                                       }
                    # ret['redirect'] = '/mylearning/mylearning/'
                return json.dumps(ret)

