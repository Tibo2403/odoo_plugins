import datetime
import importlib

import pytest


@pytest.fixture(autouse=True)
def social_post_class():
    """Reload SocialPost and reset its registry for each test."""
    from social_marketing.models import social_post
    importlib.reload(social_post)
    social_post.SocialPost._registry = []
    social_post.models.Model._id_seq = 1
    return social_post.SocialPost


def test_run_scheduled_posts_posts_due_items(social_post_class, monkeypatch):
    SocialPost = social_post_class

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


def test_run_scheduled_posts_ignores_future_items(social_post_class, monkeypatch):
    SocialPost = social_post_class

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
    assert post.stats_impressions == 0
    assert post.stats_clicks == 0
