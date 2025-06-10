import sys
import types
import datetime

# Provide minimal odoo stubs so addon modules can be imported
odoo = types.ModuleType('odoo')
models_mod = types.ModuleType('odoo.models')
class Model:
    pass
models_mod.Model = Model

fields_mod = types.ModuleType('odoo.fields')
class _Field:
    def __init__(self, *args, **kwargs):
        pass
class _Datetime:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def now():
        return datetime.datetime.now()
class Char(_Field):
    pass
class Many2one(_Field):
    pass
class Text(_Field):
    pass
class Selection(_Field):
    pass
class Integer(_Field):
    pass
class Boolean(_Field):
    pass
fields_mod.Char = Char
fields_mod.Many2one = Many2one
fields_mod.Text = Text
fields_mod.Selection = Selection
fields_mod.Integer = Integer
fields_mod.Datetime = _Datetime
fields_mod.Boolean = Boolean

api_mod = types.ModuleType('odoo.api')
api_mod.model = lambda func: func

odoo.models = models_mod
odoo.fields = fields_mod
odoo.api = api_mod

sys.modules.setdefault('odoo', odoo)
sys.modules.setdefault('odoo.models', models_mod)
sys.modules.setdefault('odoo.fields', fields_mod)
sys.modules.setdefault('odoo.api', api_mod)
