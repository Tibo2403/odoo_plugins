import datetime

import pytest
from odoo.exceptions import ValidationError


class DummyAccount:
    id = 1
    name = 'LinkedIn Company Page'


def test_social_post_requires_scheduled_date_before_scheduling(social_post_class):
    post = social_post_class(
        name='Post without date',
        account_id=DummyAccount(),
        content='Content ready to publish.',
        state='draft',
        scheduled_date=None,
        stats_impressions=0,
        stats_clicks=0,
    )

    with pytest.raises(ValidationError):
        post.action_schedule()


def test_social_post_can_be_scheduled_and_published(social_post_class):
    post = social_post_class(
        name='Scheduled post',
        account_id=DummyAccount(),
        content='Content ready to publish.',
        state='draft',
        scheduled_date=datetime.datetime.now() + datetime.timedelta(hours=1),
        stats_impressions=0,
        stats_clicks=0,
    )

    post.action_schedule()
    assert post.state == 'scheduled'

    post.action_publish()
    assert post.state == 'published'


def test_cron_publishes_due_scheduled_posts(social_post_class):
    due_post = social_post_class(
        name='Due post',
        account_id=DummyAccount(),
        content='Publish me.',
        state='scheduled',
        scheduled_date=datetime.datetime.now() - datetime.timedelta(minutes=5),
        stats_impressions=0,
        stats_clicks=0,
    )
    future_post = social_post_class(
        name='Future post',
        account_id=DummyAccount(),
        content='Not yet.',
        state='scheduled',
        scheduled_date=datetime.datetime.now() + datetime.timedelta(hours=2),
        stats_impressions=0,
        stats_clicks=0,
    )

    processed = due_post._cron_publish_scheduled_posts()

    assert processed == 1
    assert due_post.state == 'published'
    assert future_post.state == 'scheduled'
