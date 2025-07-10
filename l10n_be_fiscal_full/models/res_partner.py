from odoo import models, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _description = 'Partner'

    name = fields.Char(required=True)
    vat = fields.Char(string='VAT Number')
    street = fields.Char()
    zip = fields.Char()
    city = fields.Char()
