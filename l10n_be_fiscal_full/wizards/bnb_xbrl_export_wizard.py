from odoo import models, fields
import base64

from ..models.declaration import FiscalDeclaration


class BnbXbrlExportWizard(models.Model):
    _name = 'bnb.xbrl.export.wizard'
    _description = 'BNB XBRL Export Wizard'

    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    xbrl_taxonomy = fields.Char(string='XBRL Taxonomy', required=True)
    account_data = fields.Text(string='Account Mapping', required=True)

    def action_export(self):
        """Generate XBRL and return it as a downloadable URL."""
        dec = FiscalDeclaration(
            name=f'BNB XBRL {self.fiscal_year}',
            declaration_type='xbrl',
            xbrl_taxonomy=self.xbrl_taxonomy,
            account_data=self.account_data,
        )
        xml = dec.generate_bnb_xbrl()
        dec.export_bnb()
        data = base64.b64encode(xml.encode('utf-8')).decode('ascii')
        return {
            'type': 'ir.actions.act_url',
            'url': f'data:text/xml;base64,{data}',
            'target': 'new',
        }
