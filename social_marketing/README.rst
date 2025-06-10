Social Marketing Plugin
=======================

This addon provides basic models for managing social media accounts and posts
within Odoo, demonstrating the structure of a marketing plugin.

Features include:

- Management of social media accounts with platform selection.
- Scheduling of posts with automatic processing via a cron job.
- Simple tracking fields for impressions and clicks.
- Manual "Post Now" action for immediate publishing.

Installation
------------

1. Copy the ``social_marketing`` directory into your Odoo addons path.
2. Update the app list and install **Social Marketing** from the Apps menu.

Configuration
-------------

1. Open **Social Marketing → Configuration → Accounts**.
2. Create an account record for each social platform you intend to use.
3. Give users the *Social Marketing Manager* role so they can manage
   accounts and schedule posts.

Usage Example
-------------

1. Go to **Social Marketing → Posts** and create a new post.
2. Select the desired account and enter your message content.
3. Use **Schedule** to choose a future publish date or **Post Now** for
   immediate publication.

Scheduling
----------

The module includes a scheduled action ``social.post.scheduler`` that runs
every five minutes to publish posts whose scheduled date has passed. You can
adjust the interval from **Settings → Technical → Automation → Scheduled
Actions**.

Required Permissions
--------------------

Only members of the *Social Marketing Manager* group can configure accounts
and schedule posts. Read access to published content is granted to all internal
users.

Connecting to a Real Platform
-----------------------------

This module ships with stub methods for posting content. To integrate with an
actual platform API you would typically perform an HTTP request to the
platform's endpoint. A simplified example using ``requests`` is shown below::

    import requests

    API_ENDPOINT = "https://api.example.com/v1/post"  # Replace with real URL
    ACCESS_TOKEN = "YOUR_TOKEN"                        # Load from a safe place

    def send_post(message: str):
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        payload = {"text": message}
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()

The ``ACCESS_TOKEN`` and ``API_ENDPOINT`` values above are placeholders. When
implementing your own integration, ensure that credentials are stored securely
in environment variables or Odoo's system parameters rather than committed to
version control. Consider limiting access to these values so they are only
visible to the server running Odoo.
