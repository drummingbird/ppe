# -*- coding: utf-8 -*-
import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _

class ProgramsList(http.Controller):
    @http.route('/programs/<string(maxlength=15):category>', type='http', auth='public', website=True)
    def listPrograms(self, category):
        if category=="all": 
            domain = []
            listname = "All programs"
        if category=="individuals":
            domain = [('individual','=','true')]
            listname = "Programs for individuals"
        if category=="organisations":
            domain = [('organisational','=','true')]
            listname = "Programs for organisations"
        programs = request.env['mqo.program'].search(domain)
        if programs:
            return request.website.render('mqo_program.list', {
                'programs': programs,
                'category': category,
                'listname': listname 
            })
        else:
            return request.website.render('website.404');

