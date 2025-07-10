import pytest


@pytest.fixture
def partner_class():
    import importlib
    from l10n_be_fiscal_full.models import res_partner
    importlib.reload(res_partner)
    res_partner.ResPartner._registry = []
    res_partner.models.Model._id_seq = 1
    return res_partner.ResPartner


@pytest.fixture
def belcotax_line_class():
    import importlib
    from l10n_be_fiscal_full.models import belcotax_line
    importlib.reload(belcotax_line)
    belcotax_line.BelcotaxDeclarationLine._registry = []
    belcotax_line.models.Model._id_seq = 1
    return belcotax_line.BelcotaxDeclarationLine


def test_partner_helper_methods(partner_class, belcotax_line_class, fiscal_declaration_class):
    Partner = partner_class
    Line = belcotax_line_class
    Declaration = fiscal_declaration_class

    partner = Partner(name='Acme', vat='BE0123456789', street='Main', zip='1000', city='Brussels')
    decl = Declaration(name='Belcotax', declaration_type='belcotax')
    line = Line(declaration_id=decl, partner_id=partner, amount=42)

    assert line.get_partner_vat() == 'BE0123456789'
    assert line.get_partner_address() == 'Main, 1000, Brussels'


def test_generate_belcotax_xml_contains_partner_data(partner_class, belcotax_line_class, fiscal_declaration_class):
    Partner = partner_class
    Line = belcotax_line_class
    Declaration = fiscal_declaration_class

    partner = Partner(name='Acme', vat='BE0123456789', street='Main', zip='1000', city='Brussels')
    decl = Declaration(name='Belcotax', declaration_type='belcotax')
    line = Line(declaration_id=decl, partner_id=partner, amount=99)

    decl.belcotax_line_ids = [line]

    decl.generate_xml()

    assert 'BE0123456789' in decl.xml_content
    assert 'Main, 1000, Brussels' in decl.xml_content

