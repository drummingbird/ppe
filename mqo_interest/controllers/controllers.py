# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID

from openerp.addons.survey.controllers.main import WebsiteSurvey
import json
import logging

_logger = logging.getLogger(__name__)

class RegisterInterest(http.Controller):
    @http.route('/program/interest/<model("mqo.program"):program>', type='http', auth='public', website=True)
    def registerInterestForm(self, **kwargs):
        values = {}
        values[program] = program
        values[program_id] = program.id
        for field in ['name', 'contact_phone', 'contact_email', 'contact_org', 'message', 'program_id']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render('mqo_interest.register', values)

    def create_interest(self, request, values, kwargs):
        """ Allow to be overrided """
        cr, context = request.cr, request.context
        return request.registry['mqo_interest.interest'].create(cr, SUPERUSER_ID, values, context=dict(context, mail_create_nosubscribe=True))

    def get_interest_response(self, values, kwargs):
        return request.website.render(kwargs.get("view_callback", "mqo_interest.interest_thanks"), values)

    @http.route(['/program/registerinterest'], type='http', auth="public", website=True)
    def registerInterest(self, **kwargs):
        def dict_to_str(title, dictvar):
            ret = "\n\n%s" % title
            for field in dictvar:
                ret += "\n%s" % field
            return ret

        _TECHNICAL = ['show_info', 'view_from', 'view_callback']  # Only use for behavior, don't stock it
        _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'user_id', 'active']  # Allow in description
        _REQUIRED = ['contact_name', 'contact_email', 'program']  # Could be improved including required from model

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

        # description is required, so it is always already initialized
        if post_extra_info:
            values['extra_info'] += dict_to_str(_("Custom Fields: "), post_extra_info)

        if kwargs.get("show_info"):
            post_description = []
            environ = request.httprequest.headers.environ
            post_description.append("%s: %s" % ("IP", environ.get("REMOTE_ADDR")))
            post_description.append("%s: %s" % ("USER_AGENT", environ.get("HTTP_USER_AGENT")))
            post_description.append("%s: %s" % ("ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE")))
            post_description.append("%s: %s" % ("REFERER", environ.get("HTTP_REFERER")))
            values['description'] += dict_to_str(_("Environ Fields: "), post_description)

        interest_id = self.create_lead(request, dict(values, user_id=False), kwargs)
        values.update(interest_id=interest_id)
        return self.get_interest_response(values, kwargs)
