from odoo import fields, models


class SocialAccount(models.Model):
    _name = 'social.marketing.account'
    _description = 'Social Marketing Account'

    name = fields.Char(required=True)
    platform = fields.Selection([
        ('linkedin', 'LinkedIn'),
        ('x', 'X'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    ], default='linkedin')
    active = fields.Boolean(default=True)
