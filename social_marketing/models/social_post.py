from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SocialPost(models.Model):
    _name = 'social.marketing.post'
    _description = 'Social Marketing Post'
    _order = 'scheduled_date desc, id desc'

    name = fields.Char(required=True)
    account_id = fields.Many2one('social.marketing.account', required=True)
    content = fields.Text(required=True)
    scheduled_date = fields.Datetime()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ], default='draft', required=True)
    stats_impressions = fields.Integer(default=0)
    stats_clicks = fields.Integer(default=0)

    @api.constrains('scheduled_date', 'state')
    def _check_scheduled_date(self):
        for post in self:
            if post.state == 'scheduled' and not post.scheduled_date:
                raise ValidationError('A scheduled post must have a scheduled date.')

    def _iter_posts(self):
        """Support both real Odoo recordsets and the lightweight test stubs."""

        if isinstance(self, list):
            return self
        return [self]

    def action_schedule(self):
        for post in self._iter_posts():
            if not post.scheduled_date:
                raise ValidationError('Set a scheduled date before scheduling the post.')
            if post.state == 'published':
                raise ValidationError('A published post cannot be scheduled again.')
            post.state = 'scheduled'

    def action_publish(self):
        for post in self._iter_posts():
            if post.state == 'cancelled':
                raise ValidationError('A cancelled post cannot be published.')
            post.state = 'published'

    def action_cancel(self):
        for post in self._iter_posts():
            if post.state == 'published':
                raise ValidationError('A published post cannot be cancelled.')
            post.state = 'cancelled'

    @api.model
    def _cron_publish_scheduled_posts(self):
        """Publish scheduled posts whose planned date has been reached.

        This keeps the cron deterministic and easy to test. Real social network
        API calls should be added behind a connector/service layer before marking
        posts as published in production.
        """

        posts = self.search([
            ('state', '=', 'scheduled'),
            ('scheduled_date', '<=', fields.Datetime.now()),
        ])
        posts.action_publish()
        return len(posts)
