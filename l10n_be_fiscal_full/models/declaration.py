from odoo import models, fields


class FiscalDeclaration(models.Model):
    _name = 'be.fiscal.declaration'
    _description = 'Belgian Fiscal Declaration'

    name = fields.Char(required=True)
    declaration_type = fields.Selection([
        ('vat', 'VAT'),
        ('listing', 'Client Listing'),
        ('belcotax', 'Belcotax'),
        ('isoc', 'ISOC'),
        ('xbrl', 'XBRL')
    ], required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('exported', 'Exported')
    ], default='draft')
    xml_content = fields.Text(string='XML Content')

    def _iterate(self):
        """Return a list of records for uniform iteration."""
        return self if isinstance(self, (list, tuple)) else [self]

    def generate_xml(self):
        """Generate a very basic XML representation for the declaration."""
        for rec in self._iterate():
            rec.xml_content = (
                f"<declaration type='{rec.declaration_type}' name='{rec.name}'/>"
            )
            rec.state = 'ready'
        return getattr(self, 'xml_content', None)

    def export_xml(self):
        """Mark the declaration as exported and return its XML."""
        for rec in self._iterate():
            if rec.state != 'ready':
                rec.generate_xml()
            rec.state = 'exported'
        return getattr(self, 'xml_content', None)
