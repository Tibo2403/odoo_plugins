from odoo import models, fields


class AccountMove(models.Model):
    _name = 'account.anomaly.move'
    _description = 'Accounting Move'

    name = fields.Char(required=True)
    amount = fields.Float(required=True)
    date = fields.Date(default=fields.Date.today)
    is_anomaly = fields.Boolean(string='Anomaly', default=False)

    @classmethod
    def find_anomalies(cls, threshold=10000.0):
        """Return moves with negative amounts or exceeding ``threshold``."""
        anomalies = []
        for rec in cls._registry:
            if rec.amount < 0 or rec.amount > threshold:
                rec.is_anomaly = True
                anomalies.append(rec)
        return anomalies
