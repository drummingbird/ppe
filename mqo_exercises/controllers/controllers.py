# -*- coding: utf-8 -*-
from openerp import http


class MyLearning(http.Controller):
    @http.route('/mylearning/mylearning/', auth='public', website=True)
    def index(self, **kw):
        Exercises = http.request.env['mqo.exercise']
        return http.request.render('mqo_exercises.index', {
            'exercises': Exercises.search([])
        })