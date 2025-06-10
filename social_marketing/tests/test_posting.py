import datetime
import types
import importlib
import sys

import pytest


def setup_module(module):
    """Stub minimal des modules Odoo pour exécuter les tests."""
    odoo = types.ModuleType('odoo')
    models_mod = types.ModuleType('odoo.models')
    class Model: pass
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
    api_mod.model = lambda func: func

    odoo.models = models_mod
    odoo.fields = fields_mod
    odoo.api = api_mod

    sys.modules.setdefault('odoo', odoo)
    sys.modules.setdefault('odoo.models', models_mod)
    sys.modules.setdefault('odoo.fields', fields_mod)
    sys.modules.setdefault('odoo.api', api_mod)

    importlib.invalidate_caches()


@pytest.fixture(autouse=True)
def reset_registry():
    from social_marketing.models import social_post
    social_post.SocialPost._registry = []


def test_run_scheduled_posts_posts_due_items(monkeypatch):
    from social_marketing.models import social_post
    importlib.reload(social_post)
    SocialPost = social_post.SocialPost

    post = SocialPost(
        name='test',
        account_id=None,
        content='demo',
        scheduled_date=datetime.datetime.now() - datetime.timedelta(hours=1),
        state='scheduled',
        stats_impressions=0,
        stats_clicks=0,
    )

    monkeypatch.setattr(SocialPost, 'search', lambda self, domain: [post], raising=False)

    SocialPost().run_scheduled_posts()

    assert post.state == 'posted'
    assert post.stats_impressions == 1
    assert post.stats_clicks == 1


def test_run_scheduled_posts_ignores_future_items(monkeypatch):
    from social_marketing.models import social_post
    importlib.reload(social_post)
    SocialPost = social_post.SocialPost

    post = SocialPost(
        name='future',
        account_id=None,
        content='later',
        scheduled_date=datetime.datetime.now() + datetime.timedelta(hours=1),
        state='scheduled',
        stats_impressions=0,
        stats_clicks=0,
    )

    monkeypatch.setattr(SocialPost, 'search', lambda self, domain: [post], raising=False)

    SocialPost().run_scheduled_posts()

    assert post.state == 'scheduled'
    assert post.stats_i_
