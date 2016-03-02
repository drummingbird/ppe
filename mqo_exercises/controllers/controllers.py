# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request

class MyLearning(http.Controller):
    @http.route('/mylearning/mylearning/', auth='public', website=True)
    def index(self, **kw):
        # Partners = http.request.env['res.partner']
        partner = request.env['res.users'].browse(request.uid).partner_id
        print(str(partner.name))
        print(str(partner.id))
        if partner:
            ResPartner = request.env['res.partner'].browse(partner.id)
            currentex = ResPartner.next_exercise_id
            print(str(currentex.name))
            return request.render('mqo_exercises.index', {
                'exercises': currentex
            })
        else:
            return request.render('mqo_exercises.index', {'exercises': []})