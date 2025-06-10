import datetime
from importlib import reload

from social_marketing.models import social_post

SocialPost = social_post.SocialPost


def setup_function(function):
    SocialPost._registry = []


def test_run_scheduled_posts_posts_due_items():
    post = SocialPost(
        name='test',
        account_id=None,
        content='demo',
        scheduled_date=datetime.datetime.now() - datetime.timedelta(hours=1),
        state='scheduled',
        stats_impressions=0,
        stats_clicks=0,
    )
    SocialPost.run_scheduled_posts(SocialPost)
    assert post.state == 'posted'
    assert post.stats_impressions == 1
    assert post.stats_clicks == 1


def test_run_scheduled_posts_ignores_future_items():
    post = SocialPost(
        name='future',
        account_id=None,
        content='later',
        scheduled_date=datetime.datetime.now() + datetime.timedelta(hours=1),
        state='scheduled',
        stats_impressions=0,
        stats_clicks=0,
    )
    SocialPost.run_scheduled_posts(SocialPost)
    assert post.state == 'scheduled'

