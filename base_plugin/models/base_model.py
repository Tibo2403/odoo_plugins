from odoo import models, fields


class BaseModel(models.Model):
    _name = 'base.plugin.model'
    _description = 'Base Plugin Model'

    name = fields.Char(string='Name', required=True)
