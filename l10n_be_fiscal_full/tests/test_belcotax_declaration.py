import importlib
from odoo.fields import Date
import pytest


@pytest.fixture
def belcotax_declaration_class():
    from l10n_be_fiscal_full.models import belcotax
    importlib.reload(belcotax)
    belcotax.BelcotaxDeclaration._registry = []
    belcotax.models.Model._id_seq = 1
    return belcotax.BelcotaxDeclaration


@pytest.fixture
def partner_class():
    from l10n_be_fiscal_full.models import res_partner
    importlib.reload(res_partner)
    res_partner.ResPartner._registry = []
    res_partner.models.Model._id_seq = 1
    return res_partner.ResPartner


def test_generate_xml_contains_partner_vat(belcotax_declaration_class, partner_class):
    Partner = partner_class
    Declaration = belcotax_declaration_class

    partner = Partner(name='Foo', vat='BE0123456789')
    dec = Declaration(
        name='Test',
        fiscal_year='2022',
        form_type='281.50',
        partner_id=partner,
        amount=10,
    )

    dec.generate_xml()

    assert dec.state == 'ready'
    assert 'BE0123456789' in dec.xml_content


def test_export_xml_sets_date(belcotax_declaration_class):
    Declaration = belcotax_declaration_class
    dec = Declaration(
        name='Test',
        fiscal_year='2022',
        form_type='281.20',
        amount=5,
    )

    dec.export_xml()

    assert dec.state == 'exported'
    assert dec.exported_date == Date.today()

