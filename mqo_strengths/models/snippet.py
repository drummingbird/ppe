from openerp import models, fields, api


class Mqo_strength_snippet(models.Model):
    _name = "mqo.snippet.strengths"
    _description = "Snippets for strengths ..."

    name = fields.Char(string="Name", required=True)
    title = fields.Char(string="Title", required=True)
    subtitle = fields.Char(string="Subtitle")
    text = fields.Char(string="Text", required=True)
    value = fields.Float(string="Optional value")
