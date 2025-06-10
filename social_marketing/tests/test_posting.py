def test_post_now_transitions_states_and_updates_stats(social_post_class):
    SocialPost = social_post_class

    draft = SocialPost(
        name='draft',
        account_id=None,
        content='post 1',
        state='draft',
        scheduled_date=datetime.datetime.now(),
        stats_impressions=2,
        stats_clicks=3,
    )

    scheduled = SocialPost(
        name='scheduled',
        account_id=None,
        content='post 2',
        state='scheduled',
        scheduled_date=datetime.datetime.now(),
        stats_impressions=1,
        stats_clicks=4,
    )

    SocialPost.post_now([draft, scheduled])

    # Vérifie que les états ont bien changé
    assert draft.state == 'posted'
    assert scheduled.state == 'posted'

    # Vérifie l'incrémentation des stats
    assert draft.stats_impressions == 3  # 2 + 1
    assert draft.stats_clicks == 4       # 3 + 1

    assert scheduled.stats_impressions == 2  # 1 + 1
    assert scheduled.stats_clicks == 5       # 4 + 1
