from odoo import models, fields


class BelcotaxDeclarationLine(models.Model):
    _name = 'belcotax.declaration.line'
    _description = 'Belcotax Declaration Line'

    declaration_id = fields.Many2one('be.fiscal.declaration', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    amount = fields.Float()

    def get_partner_vat(self):
        partner = getattr(self, 'partner_id', None)
        return getattr(partner, 'vat', '') if partner else ''

    def get_partner_address(self):
        partner = getattr(self, 'partner_id', None)
        if not partner:
            return ''
        parts = [partner.street, partner.zip, partner.city]
        return ', '.join([p for p in parts if p])
