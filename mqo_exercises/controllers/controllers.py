# -*- coding: utf-8 -*-
from openerp import http


class MyLearning(http.Controller):
    @http.route('/mylearning/mylearning/', auth='public', website=True)
    def index(self, **kw):
        # Partners = http.request.env['res.partner']
        partner = http.request.env['res.users'].browse(request.uid).partner_id
        if partner:
            currentex = partner.next_exercise_id
            return http.request.render('mqo_exercises.index', {
                'exercises': currentex
            })
        else:
            return http.request.render('mqo_exercises.index', {'exercises': []})