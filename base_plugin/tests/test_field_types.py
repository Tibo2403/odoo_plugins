import datetime
from odoo import models, fields, api


def test_fields_module_contains_new_types():
    assert hasattr(fields, "Float")
    assert hasattr(fields, "Date")
    assert hasattr(fields, "Many2many")
    assert hasattr(fields, "One2many")


class DummyModel(models.Model):
    _name = 'dummy.model'

    float_field = fields.Float()
    date_field = fields.Date()
    many_ids = fields.Many2many('dummy.model')
    one_ids = fields.One2many('dummy.model', 'parent_id')
    parent_id = fields.Many2one('dummy.model')

    def __init__(self, **vals):
        super().__init__(**vals)
        self.double = 0

    @api.depends('float_field')
    def compute_double(self):
        self.double = self.float_field * 2


def test_api_depends_and_fields_usage():
    rec = DummyModel(float_field=2.5, date_field=datetime.date.today())
    rec.compute_double()
    assert rec.double == 5.0
    assert getattr(DummyModel.compute_double, '_depends') == ('float_field',)

