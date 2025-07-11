from odoo import models, fields


class BelcotaxDeclaration(models.Model):
    """Simplified Belcotax declaration used in tests."""

    _name = 'belcotax.declaration'
    _description = 'Belcotax Declaration'

    name = fields.Char(required=True)
    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    form_type = fields.Selection([
        ('281.50', '281.50'),
        ('281.20', '281.20'),
        ('281.10', '281.10'),
    ], string='Form Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    amount = fields.Float()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('exported', 'Exported'),
    ], default='draft')
    exported_date = fields.Date(string='Exported On')
    xml_content = fields.Text(string='XML Content')

    def _iterate(self):
        return self if isinstance(self, (list, tuple)) else [self]

    def generate_xml(self):
        """Create a very small XML snippet with partner and amount."""
        for rec in self._iterate():
            partner = getattr(rec.partner_id, 'name', '')
            vat = getattr(rec.partner_id, 'vat', '')
            rec.xml_content = (
                f"<Belcotax form='{rec.form_type}' year='{rec.fiscal_year}' "
                f"partner='{partner}' vat='{vat}' amount='{rec.amount}'/>"
            )
            rec.state = 'ready'
        return getattr(self, 'xml_content', None)

    def export_xml(self):
        for rec in self._iterate():
            if rec.state != 'ready':
                rec.generate_xml()
            rec.state = 'exported'
            rec.exported_date = fields.Date.today()
        return getattr(self, 'xml_content', None)
