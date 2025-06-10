import sys
import types
import datetime
import importlib


def setup_module(module):
    """Provide minimal odoo stubs for importing the addon."""
    # create base odoo modules
    odoo = types.ModuleType('odoo')
    models_mod = types.ModuleType('odoo.models')
    class Model:
        pass
    models_mod.Model = Model

    fields_mod = types.ModuleType('odoo.fields')
    class _Datetime:
        @staticmethod
        def now():
            return datetime.datetime.now()
    fields_mod.Char = object
    fields_mod.Many2one = object
    fields_mod.Text = object
    fields_mod.Selection = object
    fields_mod.Integer = object
    fields_mod.Datetime = _Datetime

    api_mod = types.ModuleType('odoo.api')
    def model(func):
        return func
    api_mod.model = model

    odoo.models = models_mod
    odoo.fields = fields_mod
    odoo.api = api_mod

    sys.modules.setdefault('odoo', odoo)
    sys.modules.setdefault('odoo.models', models_mod)
    sys.modules.setdefault('odoo.fields', fields_mod)
    sys.modules.setdefault('odoo.api', api_mod)

    # reload the module under test to apply stubs
    importlib.invalidate_caches()


def test_run_scheduled_posts(monkeypatch):
    from social_marketing.models import social_post
    importlib.reload(social_post)
    SocialPost = social_post.SocialPost

    post = types.SimpleNamespace(
        state='scheduled',
        scheduled_date=datetime.datetime.now() - datetime.timedelta(hours=1),
        stats_impressions=0,
        stats_clicks=0,
        id=1,
    )

    recordset = type('Recordset', (list,), {})([post])
    recordset.post_now = SocialPost.post_now.__get__(recordset, type(recordset))

    monkeypatch.setattr(SocialPost, 'search', lambda self, domain: recordset, raising=False)

    SocialPost().run_scheduled_posts()

    assert post.state == 'posted'
    assert post.stats_impressions == 1
    assert post.stats_clicks == 1
