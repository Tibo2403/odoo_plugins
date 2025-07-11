import xml.etree.ElementTree as ET


def test_intervat_xml_contains_values(fiscal_declaration_class):
    FiscalDeclaration = fiscal_declaration_class

    dec = FiscalDeclaration(
        name='Q1 VAT',
        declaration_type='vat',
        vat_code_00=100,
        vat_code_01=50,
        period_type='month',
        period_month='3',
    )

    dec.generate_xml()

    root = ET.fromstring(dec.xml_content)
    assert root.tag == 'VATDeclaration'
    assert root.findtext('VatCode00') == '100'
    assert root.findtext('VatCode01') == '50'
    assert root.findtext('Month') == '3'
