import sys
import types
import datetime
import pytest

# Crée un module simulé "odoo"
odoo = types.ModuleType('odoo')

# Champs simulés
class _Field:
    def __init__(self, *args, **kwargs):
        pass

class _DatetimeField(_Field):
    @staticmethod
    def now():
        return datetime.datetime.now()


class _DateField(_Field):
    @staticmethod
    def today():
        return datetime.date.today()

# Champs typés pour compatibilité avec Odoo
class Char(_Field): pass
class Many2one(_Field): pass
class Text(_Field): pass
class Selection(_Field): pass
class Integer(_Field): pass
class Boolean(_Field): pass
class Float(_Field): pass
class Many2many(_Field): pass
class One2many(_Field): pass

# Enveloppe fields
fields_mod = types.ModuleType('odoo.fields')
fields_mod.Char = Char
fields_mod.Many2one = Many2one
fields_mod.Text = Text
fields_mod.Selection = Selection
fields_mod.Integer = Integer
fields_mod.Boolean = Boolean
fields_mod.Datetime = _DatetimeField
fields_mod.Date = _DateField
fields_mod.Float = Float
fields_mod.Many2many = Many2many
fields_mod.One2many = One2many

# Décorateurs API simulés
api_mod = types.ModuleType('odoo.api')
api_mod.model = lambda f: f


def _store_args(attr):
    def decorator(*fields):
        def wrapper(func):
            setattr(func, attr, fields)
            return func
        return wrapper
    return decorator


api_mod.depends = _store_args('_depends')
api_mod.onchange = _store_args('_onchange')
api_mod.constrains = _store_args('_constrains')
api_mod.model_create_multi = lambda f: f

# RecordSet simulé (comme un ORM Odoo)
class RecordSet(list):
    def __getattr__(self, item):
        def wrapper(*args, **kwargs):
            if not self:
                return None
            method = getattr(self[0].__class__, item)
            return method(self, *args, **kwargs)
        return wrapper

# Classe Model simulée avec registre et environnement simulé
class Model:
    _registry = []
    _id_seq = 1
    env = types.SimpleNamespace(company=types.SimpleNamespace(id=1))  # simulate self.env.company.id

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

# Modules simulés
models_mod = types.ModuleType('odoo.models')
models_mod.Model = Model

# Assemble le module odoo
odoo.models = models_mod
odoo.fields = fields_mod
odoo.api = api_mod

# Injection dans sys.modules
sys.modules.setdefault('odoo', odoo)
sys.modules.setdefault('odoo.models', models_mod)
sys.modules.setdefault('odoo.fields', fields_mod)
sys.modules.setdefault('odoo.api', api_mod)


@pytest.fixture
def social_post_class():
    import importlib
    from social_marketing.models import social_post
    importlib.reload(social_post)
    social_post.SocialPost._registry = []
    social_post.models.Model._id_seq = 1
    return social_post.SocialPost
