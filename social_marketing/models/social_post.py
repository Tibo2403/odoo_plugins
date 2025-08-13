import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class SocialPost(models.Model):
    _name = 'social.marketing.post'
    _description = 'Scheduled Social Post'

    name = fields.Char(string='Title', required=True)
    account_id = fields.Many2one('social.marketing.account', required=True)
    content = fields.Text(required=True)
    scheduled_date = fields.Datetime(string='Scheduled At')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('posted', 'Posted')
    ], default='draft')
    stats_impressions = fields.Integer(string='Impressions', default=0)
    stats_clicks = fields.Integer(string='Clicks', default=0)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)

    def post_now(self):
        """Post the content immediately and update statistics."""
        for post in self:
            if post.state != 'posted':
                # Here we would integrate with APIs of each platform.
                post.state = 'posted'
                post.stats_impressions += 1
                post.stats_clicks += 1
                _logger.info("Post %s published", post.id)

    @api.model
    def run_scheduled_posts(self):
        """Publish posts whose schedule is due.

        The search domain selects posts in ``scheduled`` state with a
        ``scheduled_date`` up to the current time. When executed in a real
        Odoo environment, the domain is further restricted to the current
        company. All matching records are then published via
        :meth:`post_now`.
        """
        now = fields.Datetime.now()
        domain = [
            ('state', '=', 'scheduled'),
            ('scheduled_date', '<=', now),
            ('company_id', '=', self.env.company.id),
        ]
        posts = self.search(domain)
        posts.post_now()
        return len(posts)
