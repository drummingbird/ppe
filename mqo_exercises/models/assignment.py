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
    
    response_survey = fields.Many2one('survey.survey', string="Response survey")
    responses = fields.Many2one('survey.user_input', string="Responses")
    response_token = fields.Char(string="Token", default=lambda self: 'res' + uuid.uuid4().__str__())
    
    # can add entries (while doing the exercise) as survey responses too.

    # add function to set rating and difficulty based on responses.
    
    # Add function to set response_survey from exercise.default_exercise_survey
    
    _sql_constraints = [
        ('unique_token', 'UNIQUE (response_token)', 'A token must be unique!')
    ]