from odoo import models, fields
import json


class FiscalDeclaration(models.Model):
    _name = 'lu.fiscal.declaration'
    _description = 'Luxembourg Fiscal Declaration'

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
    exported_date = fields.Date(string='Exported On')
    xml_content = fields.Text(string='XML Content')
    xbrl_taxonomy = fields.Char(string='XBRL Taxonomy')
    account_data = fields.Text(string='Account Mapping')

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

    def generate_ecdf_xbrl(self):
        """Generate a simple eCDF XBRL snippet using ``account_data``."""
        for rec in self._iterate():
            mapping = {}
            value = getattr(rec, 'account_data', None)
            if isinstance(value, str) and value:
                try:
                    mapping = json.loads(value)
                except ValueError:
                    mapping = {}
            accounts = ''.join(
                f"<account code='{code}' balance='{balance}'/>"
                for code, balance in mapping.items()
            )
            rec.xml_content = (
                f"<xbrl taxonomy='{rec.xbrl_taxonomy or ''}'>{accounts}</xbrl>"
            )
            rec.state = 'ready'
        return getattr(self, 'xml_content', None)

    def export_ecdf(self):
        """Generate eCDF XBRL and mark the declaration as exported."""
        for rec in self._iterate():
            if rec.state != 'ready':
                rec.generate_ecdf_xbrl()
            rec.state = 'exported'
            rec.exported_date = fields.Date.today()
        return getattr(self, 'xml_content', None)
