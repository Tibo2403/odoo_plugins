import sys
import types
import datetime
import pytest

# Create a simulated "odoo" module
odoo = types.ModuleType('odoo')

# Simulated field base class
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

# Typed fields for Odoo compatibility
class Char(_Field): pass
class Many2one(_Field): pass
class Text(_Field): pass
class Selection(_Field): pass
class Integer(_Field): pass
class Boolean(_Field): pass
class Float(_Field): pass
class Many2many(_Field): pass
class One2many(_Field): pass

# Wrapper module for fields
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

# Simulated API decorators
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

# RecordSet simulation similar to the Odoo ORM
class RecordSet(list):
    def __getattr__(self, item):
        def wrapper(*args, **kwargs):
            if not self:
                return None
            method = getattr(self[0].__class__, item)
            return method(self, *args, **kwargs)
        return wrapper

# Simulated Model class with registry and environment
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

# Stub models
class ResPartnerBank(Model):
    _name = 'res.partner.bank'
    _description = 'Bank Account'

    company_id = fields_mod.Many2one('res.company')
    partner_id = fields_mod.Many2one('res.partner')
    acc_number = fields_mod.Char()

# Minimal Project stub used for linking PRINCE2 records
class Project(Model):
    _name = 'project.project'
    _description = 'Project'

    name = fields_mod.Char()

# Simulated modules
models_mod = types.ModuleType('odoo.models')
models_mod.Model = Model

# Assemble the mocked odoo module
odoo.models = models_mod
odoo.fields = fields_mod
odoo.api = api_mod

res_partner_bank_mod = types.ModuleType('odoo.addons.base.models.res_partner_bank')
res_partner_bank_mod.models = models_mod
res_partner_bank_mod.fields = fields_mod
res_partner_bank_mod.ResPartnerBank = ResPartnerBank

sys.modules.setdefault('odoo.addons.base', types.ModuleType('base'))
sys.modules.setdefault('odoo.addons.base.models', types.ModuleType('models'))
sys.modules['odoo.addons.base.models'].res_partner_bank = res_partner_bank_mod

project_mod = types.ModuleType('odoo.addons.project.models.project')
project_mod.models = models_mod
project_mod.fields = fields_mod
project_mod.Project = Project
sys.modules.setdefault('odoo.addons', types.ModuleType('odoo.addons'))
sys.modules.setdefault('odoo.addons.project', types.ModuleType('project'))
sys.modules.setdefault('odoo.addons.project.models', types.ModuleType('models'))
sys.modules['odoo.addons.project.models'].project = project_mod

# Inject into sys.modules
sys.modules.setdefault('odoo', odoo)
sys.modules.setdefault('odoo.models', models_mod)
sys.modules.setdefault('odoo.fields', fields_mod)
sys.modules.setdefault('odoo.api', api_mod)
exceptions_mod = types.ModuleType('odoo.exceptions')
class ValidationError(Exception):
    pass
exceptions_mod.ValidationError = ValidationError
sys.modules.setdefault('odoo.exceptions', exceptions_mod)
sys.modules.setdefault('odoo.addons.base.models.res_partner_bank', res_partner_bank_mod)
sys.modules.setdefault('odoo.addons.project.models.project', project_mod)

# Fixtures
@pytest.fixture
def social_post_class():
    import importlib
    from social_marketing.models import social_post
    importlib.reload(social_post)
    social_post.SocialPost._registry = []
    social_post.models.Model._id_seq = 1
    return social_post.SocialPost

@pytest.fixture
def account_move_class():
    import importlib
    from account_anomaly.models import account_move
    importlib.reload(account_move)
    account_move.AccountMove._registry = []
    account_move.models.Model._id_seq = 1
    return account_move.AccountMove

@pytest.fixture
def fiscal_declaration_class():
    import importlib
    from l10n_be_fiscal_full.models import declaration
    importlib.reload(declaration)
    declaration.FiscalDeclaration._registry = []
    declaration.models.Model._id_seq = 1
    return declaration.FiscalDeclaration

@pytest.fixture
def lu_fiscal_declaration_class():
    import importlib
    from l10n_lu_fiscal_full.models import declaration
    importlib.reload(declaration)
    declaration.FiscalDeclaration._registry = []
    declaration.models.Model._id_seq = 1
    return declaration.FiscalDeclaration

@pytest.fixture
def belcotax_export_wizard_class():
    import importlib
    from l10n_be_fiscal_full.wizards import belcotax_export_wizard
    importlib.reload(belcotax_export_wizard)
    belcotax_export_wizard.BelcotaxExportWizard._registry = []
    belcotax_export_wizard.models.Model._id_seq = 1
    return belcotax_export_wizard.BelcotaxExportWizard

@pytest.fixture
def bnb_xbrl_export_wizard_class():
    import importlib
    from l10n_be_fiscal_full.wizards import bnb_xbrl_export_wizard
    importlib.reload(bnb_xbrl_export_wizard)
    bnb_xbrl_export_wizard.BnbXbrlExportWizard._registry = []
    bnb_xbrl_export_wizard.models.Model._id_seq = 1
    return bnb_xbrl_export_wizard.BnbXbrlExportWizard

@pytest.fixture
def prince2_project_class():
    import importlib
    from project_prince2.models import prince2_project
    importlib.reload(prince2_project)
    prince2_project.Prince2Project._registry = []
    prince2_project.models.Model._id_seq = 1
    return prince2_project.Prince2Project

@pytest.fixture
def partner_bank_class():
    from odoo.addons.base.models import res_partner_bank
    res_partner_bank.ResPartnerBank._registry = []
    res_partner_bank.models.Model._id_seq = 1
    return res_partner_bank.ResPartnerBank


@pytest.fixture
def project_class():
    from odoo.addons.project.models import project
    project.Project._registry = []
    project.models.Model._id_seq = 1
    return project.Project
