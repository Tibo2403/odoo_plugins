import pytest
import json
from odoo.fields import Date


def test_generate_xml_sets_content_and_state(lu_fiscal_declaration_class, monkeypatch):
    FiscalDeclaration = lu_fiscal_declaration_class

    dec = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.generate_xml()

    assert dec.xml_content.startswith('<declaration')
    assert dec.state == 'ready'


def test_export_xml_marks_exported(lu_fiscal_declaration_class, monkeypatch):
    FiscalDeclaration = lu_fiscal_declaration_class

    dec = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.export_xml()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<declaration')


def test_generate_and_export_on_list(lu_fiscal_declaration_class):
    """Methods should operate on lists of declarations."""
    FiscalDeclaration = lu_fiscal_declaration_class

    dec1 = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')
    dec2 = FiscalDeclaration(name='Client Listing', declaration_type='listing')

    class RecordList(list):
        def _iterate(self):
            return self

    records = RecordList([dec1, dec2])

    FiscalDeclaration.generate_xml(records)

    assert dec1.state == 'ready'
    assert dec2.state == 'ready'
    assert dec1.xml_content.startswith('<declaration')
    assert dec2.xml_content.startswith('<declaration')

    FiscalDeclaration.export_xml(records)

    assert dec1.state == 'exported'
    assert dec2.state == 'exported'
    assert dec1.xml_content.startswith('<declaration')
    assert dec2.xml_content.startswith('<declaration')


def test_generate_ecdf_xbrl_uses_account_data(lu_fiscal_declaration_class):
    FiscalDeclaration = lu_fiscal_declaration_class
    data = {"100": 10, "200": 20}
    dec = FiscalDeclaration(
        name='eCDF',
        declaration_type='xbrl',
        xbrl_taxonomy='lu.ecdf.test',
        account_data=json.dumps(data),
    )

    xml = dec.generate_ecdf_xbrl()

    assert xml.startswith('<xbrl')
    assert "account code='100'" in xml
    assert dec.state == 'ready'


def test_export_ecdf_generates_when_needed(lu_fiscal_declaration_class):
    FiscalDeclaration = lu_fiscal_declaration_class
    dec = FiscalDeclaration(name='eCDF', declaration_type='xbrl')

    dec.export_ecdf()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<xbrl')
    assert dec.exported_date == Date.today()
