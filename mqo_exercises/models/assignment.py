# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime, timedelta

import uuid


class Assignment(models.Model):
    _name = 'mqo.assignment'
    
    learner = fields.Many2one('mqo.learner', string="Learner", required=True)
    exercise_id = fields.Many2one('mqo.exercise',
        ondelete='cascade', string="Exercise", required=True)
    state =  fields.Selection([('new', 'Not started yet'),
                               ('skip', 'Skipped'),
                               ('done', 'Completed')],
                               string='Status', readonly=True)
    rating = fields.Float(string="Rating")
    difficulty = fields.Float(string="Difficulty")
    datetime_allocated = fields.Datetime(string="Date Time Stamp", required=True, default=lambda self: fields.Datetime.now())
    _order = "datetime_allocated desc"
