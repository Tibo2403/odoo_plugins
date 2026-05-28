from odoo import fields, models


class SocialPost(models.Model):
    _name = 'social.marketing.post'
    _description = 'Social Marketing Post'

    name = fields.Char(required=True)
    account_id = fields.Many2one('social.marketing.account')
    content = fields.Text(required=True)
    scheduled_date = fields.Datetime()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ], default='draft')
    stats_impressions = fields.Integer(default=0)
    stats_clicks = fields.Integer(default=0)

    def action_schedule(self):
        self.state = 'scheduled'

    def action_publish(self):
        self.state = 'published'

    def action_cancel(self):
        self.state = 'cancelled'
