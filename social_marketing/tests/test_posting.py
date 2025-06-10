import datetime


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


def test_post_now_updates_states_and_counters(social_post_class):
    SocialPost = social_post_class

    draft = SocialPost(
        name='draft',
        account_id=None,
        content='demo',
        scheduled_date=datetime.datetime.now(),
        state='draft',
        stats_impressions=2,
        stats_clicks=3,
    )
    scheduled = SocialPost(
        name='scheduled',
        account_id=None,
        content='demo',
        scheduled_date=datetime.datetime.now(),
        state='scheduled',
        stats_impressions=1,
        stats_clicks=4,
    )

    SocialPost.post_now([draft, scheduled])

    assert draft.state == 'posted'
    assert scheduled.state == 'posted'
    assert draft.stats_impressions == 3
    assert draft.stats_clicks == 4
    assert scheduled.stats_impressions == 2
    assert scheduled.stats_clicks == 5
