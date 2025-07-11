from odoo import models, fields
import base64

from ..models.belcotax import BelcotaxDeclaration as FiscalDeclaration


class BelcotaxExportWizard(models.Model):
    _name = 'belcotax.export.wizard'
    _description = 'Belcotax Export Wizard'

    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    form_type = fields.Selection([
        ('281.50', '281.50'),
        ('281.20', '281.20'),
    ], string='Form Type', required=True)

    def action_export(self):
        """Generate XML and return it as a downloadable URL."""
        dec = FiscalDeclaration(
            name=f'Belcotax {self.fiscal_year}',
            fiscal_year=self.fiscal_year,
            form_type=self.form_type,
        )
        xml = dec.generate_xml()
        dec.export_xml()
        data = base64.b64encode(xml.encode('utf-8')).decode('ascii')
        return {
            'type': 'ir.actions.act_url',
            'url': f'data:text/xml;base64,{data}',
            'target': 'new',
        }

