from odoo import models, fields


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
    stats_impressions = fields.Integer(string='Impressions')
    stats_clicks = fields.Integer(string='Clicks')

    def run_scheduled_posts(self):
        posts = self.search([
            ('state', '=', 'scheduled'),
            ('scheduled_date', '<=', fields.Datetime.now())
        ])
        for post in posts:
            # Here we would integrate with APIs of each platform.
            # For demonstration, we simply mark as posted.
            post.state = 'posted'
            # Increment dummy stats to simulate success
            post.stats_impressions += 1
            post.stats_clicks += 1

