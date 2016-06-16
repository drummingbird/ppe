from openerp import fields, models, api

class Benefit(models.Model):
    _name = 'mqo.benefit'

    name = fields.Char(string="Benefit")
    category =  fields.Selection([('individual', 'Individual'),
                               ('team', 'Team'),
                               ('leader', 'Leader'),
                               ('organisation', 'Organisation')],
                               string='Category')
    program_links = fields.One2many('mqo.benefit_program_link', 'benefit', string="program_links")

class BenefitProgramLink(models.Model):
    _name = 'mqo.benefit_program_link'

    program = fields.Many2one('mqo.program', string="Program")
    benefit = fields.Many2one('mqo.benefit', string="Benefit")
    sequence = fields.Integer(string="Sequence")
    
