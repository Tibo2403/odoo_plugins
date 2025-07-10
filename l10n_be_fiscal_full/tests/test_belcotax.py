import xml.etree.ElementTree as ET


def test_generate_xml_sets_content_and_state(belcotax_declaration_class, monkeypatch):
    Belcotax = belcotax_declaration_class

    partner = type('Partner', (), {'name': 'Supplier'})()
    dec = Belcotax(name='Test', fiscal_year='2023', form_type='281_50', partner_id=partner, amount=100.0)

    dec.generate_xml()

    assert dec.state == 'ready'
    root = ET.fromstring(dec.xml_content)
    assert root.tag == 'BelcotaxDeclaration'
    assert root.attrib['year'] == '2023'


def test_export_xml_marks_exported(belcotax_declaration_class):
    Belcotax = belcotax_declaration_class

    partner = type('Partner', (), {'name': 'Employee'})()
    dec = Belcotax(name='Test', fiscal_year='2023', form_type='281_20', partner_id=partner, amount=50.0)

    dec.export_xml()

    assert dec.state == 'exported'
    assert dec.xml_content.startswith('<BelcotaxDeclaration')


def test_export_year_form_collects_records(belcotax_declaration_class):
    Belcotax = belcotax_declaration_class

    partner = type('Partner', (), {'name': 'Foo'})()
    rec1 = Belcotax(name='One', fiscal_year='2023', form_type='281_50', partner_id=partner, amount=10)
    rec2 = Belcotax(name='Two', fiscal_year='2023', form_type='281_50', partner_id=partner, amount=20)

    xml = Belcotax.export_year_form('2023', '281_50')

    root = ET.fromstring(xml)
    assert root.tag == 'Belcotax'
    assert len(root.findall('BelcotaxDeclaration')) == 2
    assert rec1.state == 'exported'
    assert rec2.state == 'exported'
