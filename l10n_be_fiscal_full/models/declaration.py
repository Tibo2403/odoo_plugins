from odoo import models, fields
import json
from xml.etree.ElementTree import Element, SubElement, tostring


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
    exported_date = fields.Date(string='Exported On')
    xml_content = fields.Text(string='XML Content')
    xbrl_taxonomy = fields.Char(string='XBRL Taxonomy')
    account_data = fields.Text(string='Account Mapping')
    belcotax_line_ids = fields.One2many(
        'belcotax.declaration.line', 'declaration_id', string='Belcotax Lines'
    )
    # VAT specific fields
    vat_code_00 = fields.Float(string='Code 00')
    vat_code_01 = fields.Float(string='Code 01')
    vat_code_54 = fields.Float(string='Code 54')
    intra_eu_sales = fields.Float(string='Intra-EU Sales')
    intra_eu_purchases = fields.Float(string='Intra-EU Purchases')
    exempt_sales = fields.Float(string='Exempt Sales')
    period_type = fields.Selection([
        ('month', 'Month'),
        ('quarter', 'Quarter'),
    ], default='month', string='Period Type')
    period_month = fields.Selection(
        [(str(i), str(i)) for i in range(1, 13)], string='Month'
    )
    period_quarter = fields.Selection(
        [('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')],
        string='Quarter'
    )

    def _iterate(self):
        """Return a list of records for uniform iteration."""
        return self if isinstance(self, (list, tuple)) else [self]

    def generate_xml(self):
        """Generate an XML representation for the declaration."""
        for rec in self._iterate():
            if rec.declaration_type == 'vat':
                root = Element('VATDeclaration')
                period_type = rec.__dict__.get('period_type', '')
                SubElement(root, 'PeriodType').text = period_type or ''
                if period_type == 'month':
                    month = rec.__dict__.get('period_month', '')
                    SubElement(root, 'Month').text = month or ''
                else:
                    quarter = rec.__dict__.get('period_quarter', '')
                    SubElement(root, 'Quarter').text = quarter or ''
                SubElement(root, 'VatCode00').text = str(rec.__dict__.get('vat_code_00', 0) or 0)
                SubElement(root, 'VatCode01').text = str(rec.__dict__.get('vat_code_01', 0) or 0)
                SubElement(root, 'VatCode54').text = str(rec.__dict__.get('vat_code_54', 0) or 0)
                SubElement(root, 'IntraEUSales').text = str(rec.__dict__.get('intra_eu_sales', 0) or 0)
                SubElement(root, 'IntraEUPurchases').text = str(rec.__dict__.get('intra_eu_purchases', 0) or 0)
                SubElement(root, 'ExemptSales').text = str(rec.__dict__.get('exempt_sales', 0) or 0)
                rec.xml_content = tostring(root, encoding='unicode')
            elif rec.declaration_type == 'belcotax':
                lines_xml = ''
                for line in getattr(rec, 'belcotax_line_ids', []):
                    vat = line.get_partner_vat()
                    addr = line.get_partner_address()
                    partner_name = getattr(line.partner_id, 'name', '')
                    lines_xml += (
                        f"<line partner='{partner_name}' vat='{vat}' "
                        f"address='{addr}' amount='{line.amount}'/>"
                    )
                rec.xml_content = (
                    f"<declaration type='{rec.declaration_type}' name='{rec.name}'>"
                    f"{lines_xml}</declaration>"
                )
            else:
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
            rec.exported_date = fields.Date.today()
        return getattr(self, 'xml_content', None)

    def generate_bnb_xbrl(self):
        """Generate a simple BNB/CBN XBRL snippet using ``account_data``."""
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

    def export_bnb(self):
        """Generate BNB XBRL and mark the declaration as exported."""
        for rec in self._iterate():
            if rec.state != 'ready':
                rec.generate_bnb_xbrl()
            rec.state = 'exported'
            rec.exported_date = fields.Date.today()
        return getattr(self, 'xml_content', None)

