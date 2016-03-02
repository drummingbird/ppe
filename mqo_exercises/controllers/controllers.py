# -*- coding: utf-8 -*-
from openerp import http


class MyLearning(http.Controller):
    @http.route('/mylearning/mylearning/', auth='public', website=True)
    def index(self, **kw):
        Partners = http.request.env['res_partner']
        currentuser = Partners.search([('name', '=', 'Tester 4')])
        currentex = currentuser.next_exercise_id
        return http.request.render('mqo_exercises.index', {
            'exercises': currentex
        })