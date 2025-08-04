from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json
try:
    from lxml import etree as ET  # type: ignore
except Exception:  # pragma: no cover - fallback when lxml isn't installed
    import xml.etree.ElementTree as ET  # noqa: N818


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

    @api.constrains(
        'vat_code_00', 'vat_code_01', 'vat_code_54',
        'intra_eu_sales', 'intra_eu_purchases', 'exempt_sales'
    )
    def _check_positive_values(self):
        for rec in self._iterate():
            for field_name in [
                'vat_code_00', 'vat_code_01', 'vat_code_54',
                'intra_eu_sales', 'intra_eu_purchases', 'exempt_sales',
            ]:
                value = getattr(rec, field_name, 0)
                if value is not None and value < 0:
                    raise ValidationError(
                        f"{field_name} must be a positive number"
                    )

    def _iterate(self):
        """Return a list of records for uniform iteration."""
        return self if isinstance(self, (list, tuple)) else [self]

    @staticmethod
    def _safe_getattr(record, name, default):
        """Retrieve ``name`` from ``record`` using ``getattr`` and fall back
        to ``default`` when the fetched value corresponds to an Odoo field
        descriptor. This mirrors the previous ``record.__dict__.get`` usage
        without directly touching ``__dict__``.
        """
        value = getattr(record, name, default)
        field_types = (
            fields.Char,
            fields.Selection,
            fields.Float,
            fields.Text,
            fields.Many2one,
            fields.Many2many,
            fields.One2many,
            fields.Datetime,
            fields.Date,
            fields.Integer,
            fields.Boolean,
        )
        if isinstance(value, field_types):
            return default
        return value

    def generate_xml(self):
        """Generate an XML representation for the declaration."""
        for rec in self._iterate():
            if rec.declaration_type == 'vat':
                root = ET.Element('VATDeclaration')
                period_type = type(rec)._safe_getattr(rec, 'period_type', '')
                ET.SubElement(root, 'PeriodType').text = period_type or ''
                if period_type == 'month':
                    month = type(rec)._safe_getattr(rec, 'period_month', '')
                    ET.SubElement(root, 'Month').text = month or ''
                else:
                    quarter = type(rec)._safe_getattr(rec, 'period_quarter', '')
                    ET.SubElement(root, 'Quarter').text = quarter or ''
                ET.SubElement(root, 'VatCode00').text = str(type(rec)._safe_getattr(rec, 'vat_code_00', 0) or 0)
                ET.SubElement(root, 'VatCode01').text = str(type(rec)._safe_getattr(rec, 'vat_code_01', 0) or 0)
                ET.SubElement(root, 'VatCode54').text = str(type(rec)._safe_getattr(rec, 'vat_code_54', 0) or 0)
                ET.SubElement(root, 'IntraEUSales').text = str(type(rec)._safe_getattr(rec, 'intra_eu_sales', 0) or 0)
                ET.SubElement(root, 'IntraEUPurchases').text = str(type(rec)._safe_getattr(rec, 'intra_eu_purchases', 0) or 0)
                ET.SubElement(root, 'ExemptSales').text = str(type(rec)._safe_getattr(rec, 'exempt_sales', 0) or 0)
                rec.xml_content = ET.tostring(root, encoding='unicode')
            elif rec.declaration_type == 'belcotax':
                root = ET.Element('declaration', type=rec.declaration_type, name=rec.name)
                for line in getattr(rec, 'belcotax_line_ids', []):
                    vat = line.get_partner_vat()
                    addr = line.get_partner_address()
                    partner_name = getattr(line.partner_id, 'name', '')
                    ET.SubElement(
                        root,
                        'line',
                        partner=partner_name,
                        vat=vat,
                        address=addr,
                        amount=str(line.amount),
                    )
                rec.xml_content = ET.tostring(root, encoding='unicode')
            else:
                root = ET.Element('declaration', type=rec.declaration_type, name=rec.name)
                rec.xml_content = ET.tostring(root, encoding='unicode')
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
            taxonomy = type(rec)._safe_getattr(rec, 'xbrl_taxonomy', '') or ''
            root = ET.Element('xbrl', taxonomy=str(taxonomy))
            for code, balance in mapping.items():
                ET.SubElement(
                    root,
                    'account',
                    code=str(code),
                    balance=str(balance),
                )
            rec.xml_content = ET.tostring(root, encoding='unicode')
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

