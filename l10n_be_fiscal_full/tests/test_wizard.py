import base64
from odoo.fields import Date


def test_belcotax_wizard_returns_act_url(belcotax_export_wizard_class, monkeypatch):
    Wizard = belcotax_export_wizard_class

    class DummyDeclaration:
        last = None

        def __init__(self, **vals):
            DummyDeclaration.last = self
            self.exported_date = None
            self.state = 'draft'

        def generate_xml(self):
            return '<xml/>'

        def export_xml(self):
            self.state = 'exported'
            self.exported_date = Date.today()
            return '<xml/>'

    module = __import__(Wizard.__module__, fromlist=[''])
    monkeypatch.setattr(module, 'FiscalDeclaration', DummyDeclaration)

    wiz = Wizard(fiscal_year='2022', form_type='281.50')
    result = wiz.action_export()

    assert result['type'] == 'ir.actions.act_url'
    assert result['url'].startswith('data:text/xml;base64,')
    data = result['url'].split(',', 1)[1]
    assert base64.b64decode(data).decode() == '<xml/>'
    assert DummyDeclaration.last.exported_date == Date.today()

