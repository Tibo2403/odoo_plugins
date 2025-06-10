from odoo import models, fields


class SocialAccount(models.Model):
    _name = 'social.marketing.account'
    _description = 'Social Media Account'

    name = fields.Char(required=True)
    platform = fields.Selection([
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'X/Twitter')
    ], required=True)
    access_token = fields.Char(string='Access Token')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
