import pytest
from odoo.fields import Date


def test_generate_xml_sets_content_and_state(fiscal_declaration_class, monkeypatch):
    FiscalDeclaration = fiscal_declaration_class

    dec = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.generate_xml()

    assert dec.xml_content.startswith('<VATDeclaration')
    assert dec.state == 'ready'


def test_export_xml_marks_exported(fiscal_declaration_class, monkeypatch):
    FiscalDeclaration = fiscal_declaration_class

    dec = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.export_xml()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<VATDeclaration')
    assert dec.exported_date == Date.today()


def test_generate_and_export_on_list(fiscal_declaration_class):
    """Methods should operate on lists of declarations."""
    FiscalDeclaration = fiscal_declaration_class

    dec1 = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')
    dec2 = FiscalDeclaration(name='Client Listing', declaration_type='listing')

    class RecordList(list):
        def _iterate(self):
            return self

    records = RecordList([dec1, dec2])

    FiscalDeclaration.generate_xml(records)

    assert dec1.state == 'ready'
    assert dec2.state == 'ready'
    assert dec1.xml_content.startswith('<VATDeclaration')
    assert dec2.xml_content.startswith('<declaration')

    FiscalDeclaration.export_xml(records)

    assert dec1.state == 'exported'
    assert dec2.state == 'exported'
    assert dec1.xml_content.startswith('<VATDeclaration')
    assert dec2.xml_content.startswith('<declaration')
    assert dec1.exported_date == Date.today()
    assert dec2.exported_date == Date.today()
