import json
from odoo.fields import Date


def test_generate_bnb_xbrl_uses_account_data(fiscal_declaration_class):
    FiscalDeclaration = fiscal_declaration_class
    data = {"100": 10, "200": 20}
    dec = FiscalDeclaration(
        name='BNB',
        declaration_type='xbrl',
        xbrl_taxonomy='be.bnb.test',
        account_data=json.dumps(data),
    )

    xml = dec.generate_bnb_xbrl()

    assert xml.startswith('<xbrl')
    assert 'account code="100"' in xml
    assert dec.state == 'ready'


def test_export_bnb_generates_when_needed(fiscal_declaration_class):
    FiscalDeclaration = fiscal_declaration_class
    dec = FiscalDeclaration(name='BNB', declaration_type='xbrl')

    dec.export_bnb()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<xbrl')
    assert dec.exported_date == Date.today()
