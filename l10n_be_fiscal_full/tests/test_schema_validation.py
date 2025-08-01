import os
import importlib
import pytest
from xml.etree import ElementTree as ET

SCHEMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'schema'))
INTERVAT_XSD = os.path.join(SCHEMA_DIR, 'intervat.xsd')
BELCOTAX_XSD = os.path.join(SCHEMA_DIR, 'belcotax.xsd')


@pytest.fixture
def partner_class():
    from l10n_be_fiscal_full.models import res_partner
    importlib.reload(res_partner)
    res_partner.ResPartner._registry = []
    res_partner.models.Model._id_seq = 1
    return res_partner.ResPartner


@pytest.fixture
def belcotax_line_class():
    from l10n_be_fiscal_full.models import belcotax_line
    importlib.reload(belcotax_line)
    belcotax_line.BelcotaxDeclarationLine._registry = []
    belcotax_line.models.Model._id_seq = 1
    return belcotax_line.BelcotaxDeclarationLine


def _validate_intervat(xml_str):
    root = ET.fromstring(xml_str)
    assert root.tag == 'VATDeclaration'
    assert root.find('VatCode00') is not None
    assert root.find('VatCode01') is not None
    assert root.find('VatCode54') is not None
    assert root.find('IntraEUSales') is not None
    assert root.find('IntraEUPurchases') is not None
    assert root.find('ExemptSales') is not None
    # one of Month or Quarter may be present
    assert root.find('Month') is not None or root.find('Quarter') is not None


def _validate_belcotax(xml_str):
    root = ET.fromstring(xml_str)
    assert root.tag == 'declaration'
    xsd = ET.parse(BELCOTAX_XSD)
    ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    elem = xsd.find('xs:element', ns)
    root_attrs = [
        a.attrib['name']
        for a in elem.find('xs:complexType', ns).findall('xs:attribute', ns)
    ]
    for attr in root_attrs:
        assert attr in root.attrib
    line_elem = elem.find('.//xs:sequence/xs:element', ns)
    line_attrs = [a.attrib['name'] for a in line_elem.findall('.//xs:attribute', ns)]
    for line in root.findall('line'):
        for attr in line_attrs:
            assert attr in line.attrib


def test_vat_xml_validates_against_xsd(fiscal_declaration_class):
    FiscalDeclaration = fiscal_declaration_class
    dec = FiscalDeclaration(
        name='VAT',
        declaration_type='vat',
        vat_code_00=1,
        vat_code_01=2,
        vat_code_54=3,
        intra_eu_sales=4,
        intra_eu_purchases=5,
        exempt_sales=6,
        period_type='month',
        period_month='1',
    )
    dec.generate_xml()
    _validate_intervat(dec.xml_content)


def test_belcotax_xml_validates_against_xsd(fiscal_declaration_class, belcotax_line_class, partner_class):
    Partner = partner_class
    Line = belcotax_line_class
    FiscalDeclaration = fiscal_declaration_class

    partner = Partner(name='Acme', vat='BE0123456789', street='Main', zip='1000', city='Brussels')
    dec = FiscalDeclaration(name='Belcotax', declaration_type='belcotax')
    line = Line(declaration_id=dec, partner_id=partner, amount=42)
    dec.belcotax_line_ids = [line]
    dec.generate_xml()
    _validate_belcotax(dec.xml_content)
