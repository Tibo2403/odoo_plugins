import pytest


def test_generate_xml_sets_content_and_state(fiscal_declaration_class, monkeypatch):
    FiscalDeclaration = fiscal_declaration_class

    dec = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.generate_xml()

    assert dec.xml_content.startswith('<declaration')
    assert dec.state == 'ready'


def test_export_xml_marks_exported(fiscal_declaration_class, monkeypatch):
    FiscalDeclaration = fiscal_declaration_class

    dec = FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.export_xml()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<declaration')
