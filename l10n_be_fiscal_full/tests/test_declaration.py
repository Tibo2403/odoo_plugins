import pytest


def test_generate_xml_sets_content_and_state(monkeypatch):
    from l10n_be_fiscal_full.models import declaration
    import importlib
    importlib.reload(declaration)
    declaration.FiscalDeclaration._registry = []
    declaration.models.Model._id_seq = 1

    dec = declaration.FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.generate_xml()

    assert dec.xml_content.startswith('<declaration')
    assert dec.state == 'ready'


def test_export_xml_marks_exported(monkeypatch):
    from l10n_be_fiscal_full.models import declaration
    import importlib
    importlib.reload(declaration)
    declaration.FiscalDeclaration._registry = []
    declaration.models.Model._id_seq = 1

    dec = declaration.FiscalDeclaration(name='Q1 VAT', declaration_type='vat')

    dec.export_xml()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<declaration')
