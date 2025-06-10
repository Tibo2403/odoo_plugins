import sys
import types
import datetime

odoo = types.ModuleType('odoo')

class _Field:
    def __init__(self, *args, **kwargs):
        pass

class _DateTimeField:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def now():
        return datetime.datetime.now()

class _Fields(types.SimpleNamespace):
    Char = _Field
    Many2one = _Field
    Text = _Field
    Selection = _Field
    Boolean = _Field
    Datetime = _DateTimeField
    Integer = _Field

class RecordSet(list):
    def __getattr__(self, item):
        def wrapper(*args, **kwargs):
            if not self:
                return None
            method = getattr(self[0].__class__, item)
            return method(self, *args, **kwargs)
        return wrapper

class Model:
    _registry = []
    _id_seq = 1

    def __init__(self, **vals):
        self.id = Model._id_seq
        Model._id_seq += 1
        for k, v in vals.items():
            setattr(self, k, v)
        self.__class__._registry.append(self)

    @classmethod
    def search(cls, domain):
        res = []
        for rec in cls._registry:
            match = True
            for field, op, value in domain:
                val = getattr(rec, field)
                if op == '=' and val != value:
                    match = False
                    break
                if op == '<=' and val > value:
                    match = False
                    break
            if match:
                res.append(rec)
        return RecordSet(res)

api = types.SimpleNamespace(model=lambda f: f)

odoo.models = types.SimpleNamespace(Model=Model)
odoo.fields = _Fields()
odoo.api = api

sys.modules.setdefault('odoo', odoo)
sys.modules.setdefault('odoo.models', odoo.models)
sys.modules.setdefault('odoo.fields', odoo.fields)
sys.modules.setdefault('odoo.api', odoo.api)
