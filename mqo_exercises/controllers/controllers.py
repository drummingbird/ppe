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
    @http.route(['/assignment/rating/<model("mqo.assignment"):assignment>'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit(self, assignment, **post):
        _logger.debug('Incoming data: %s', post)
        cr, uid, context = request.cr, request.uid, request.context
        ret = {}
        
        if post['rating']:
            assignment.write({'rating': post['rating']})
            ret['reply'] = 'This worked!'
        return json.dumps(ret)
