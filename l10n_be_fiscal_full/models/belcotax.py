from odoo import models, fields
import xml.etree.ElementTree as ET


class BelcotaxDeclaration(models.Model):
    _name = 'belcotax.declaration'
    _description = 'Belcotax Declaration'

    name = fields.Char(required=True)
    fiscal_year = fields.Char(required=True)
    form_type = fields.Selection([
        ('281_50', '281.50'),
        ('281_20', '281.20'),
    ], required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    amount = fields.Float()
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
        """Generate XML for Belcotax according to simplified XSD."""
        for rec in self._iterate():
            root = ET.Element('BelcotaxDeclaration',
                              year=str(rec.fiscal_year),
                              form=rec.form_type)
            ET.SubElement(root, 'Partner').text = getattr(rec.partner_id, 'name', '')
            ET.SubElement(root, 'Amount').text = str(rec.amount or 0)
            rec.xml_content = ET.tostring(root, encoding='unicode')
            rec.state = 'ready'
        return getattr(self, 'xml_content', None)

    def export_xml(self):
        """Mark the declaration as exported and return its XML."""
        for rec in self._iterate():
            if rec.state != 'ready':
                rec.generate_xml()
            rec.state = 'exported'
        return getattr(self, 'xml_content', None)

    @classmethod
    def export_year_form(cls, fiscal_year, form_type, pdf_preview=False):
        """Export declarations for a given fiscal year and form type."""
        records = cls.search([
            ('fiscal_year', '=', fiscal_year),
            ('form_type', '=', form_type),
        ])
        for rec in records:
            rec.export_xml()
        root = ET.Element('Belcotax')
        for rec in records:
            if rec.xml_content:
                root.append(ET.fromstring(rec.xml_content))
        xml_result = ET.tostring(root, encoding='unicode')
        if pdf_preview:
            return xml_result, 'PDF preview not implemented'
        return xml_result
