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
