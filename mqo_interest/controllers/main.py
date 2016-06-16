# -*- coding: utf-8 -*-
import base64

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _

class Interest(http.Controller):
    @http.route('/interest/<model("mqo.program"):selectedprogram>', type='http', auth='public', website=True)
    def registerInterestForm(self, selectedprogram, **kwargs):
        values = {}
        
        for field in ['name', 'contact_phone', 'contact_email', 'contact_org', 'message', 'program', 'program_name']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())

        if selectedprogram:
            values['program'] = selectedprogram.id
            values['program_name'] = selectedprogram.name
        
        return request.website.render('mqo_interest.register', values)

    def create_interest(self, request, values, kwargs):
        """ Allow to be overrided """
        cr, context = request.cr, request.context
        return request.registry['mqo.interest'].create(cr, SUPERUSER_ID, values, context=dict(context, mail_create_nosubscribe=True))

    def get_interest_response(self, values, kwargs):
        return request.website.render(kwargs.get("view_callback", "mqo_interest.interest_thanks"), values)

    @http.route(['/interest/register'], type='http', auth="public", website=True)
    def InterestRegister(self, **kwargs):
        def dict_to_str(title, dictvar):
            ret = "\n\n%s" % title
            for field in dictvar:
                ret += "\n%s" % field
            return ret

        _TECHNICAL = ['show_info', 'view_from', 'view_callback']  # Only use for behavior, don't stock it
        _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'user_id', 'active']  # Allow in description
        _REQUIRED = ['name', 'contact_email', 'program']  # Could be improved including required from model

        post_extra_info = []  # Info to add after the message
        values = {}

        for field_name, field_value in kwargs.items():
            if field_name in request.registry['mqo.interest']._fields and field_name not in _BLACKLIST:
                values[field_name] = field_value
            elif field_name not in _TECHNICAL:  # allow to add some free fields or blacklisted field like ID
                post_extra_info.append("%s: %s" % (field_name, field_value))
       
        # fields validation : Check that required field from model crm_lead exists
        error = set(field for field in _REQUIRED if not values.get(field))

        if error:
            values = dict(values, error=error, kwargs=kwargs.items())
            return request.website.render(kwargs.get("view_from", "mqo_interest.register"), values)
        
        values['extra_info'] = []
        if post_extra_info:
            values['extra_info'] += dict_to_str(_("Custom Fields: "), post_extra_info)

       
        if kwargs.get("show_info"):
            post_extra_info = []
            environ = request.httprequest.headers.environ
            post_extra_info.append("%s: %s" % ("IP", environ.get("REMOTE_ADDR")))
            post_extra_info.append("%s: %s" % ("USER_AGENT", environ.get("HTTP_USER_AGENT")))
            post_extra_info.append("%s: %s" % ("ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE")))
            post_extra_info.append("%s: %s" % ("REFERER", environ.get("HTTP_REFERER")))
            values['extra_info'] += dict_to_str(_("Environ Fields: "), post_extra_info)

        interest_id = self.create_interest(request, dict(values, user_id=False), kwargs)
        values.update(interest_id=interest_id)
        return self.get_interest_response(values, kwargs)
