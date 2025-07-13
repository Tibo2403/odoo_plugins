from odoo import models, fields


class AnomalyScanner(models.Model):
    """Aggregate simple consistency checks across modules."""

    _name = 'anomaly.scanner'
    _description = 'Anomaly Scanner'

    @staticmethod
    def scan_all():
        """Return a list describing all detected issues."""
        issues = []

        # Duplicate bank accounts
        try:
            from odoo.addons.base.models import res_partner_bank
            seen = {}
            for rec in res_partner_bank.ResPartnerBank._registry:
                num = getattr(rec, 'acc_number', None)
                if not num:
                    continue
                seen.setdefault(num, []).append(rec)
            for num, recs in seen.items():
                if len(recs) > 1:
                    issues.append({
                        'model': 'res.partner.bank',
                        'issue': 'duplicate_acc_number',
                        'acc_number': num,
                        'ids': [r.id for r in recs],
                    })
        except Exception:
            pass

        # Scheduled posts still pending in the past
        try:
            from social_marketing.models import social_post
            now = fields.Datetime.now()
            for post in social_post.SocialPost._registry:
                date = getattr(post, 'scheduled_date', None)
                if post.state == 'scheduled' and date and date <= now:
                    issues.append({
                        'model': 'social.marketing.post',
                        'issue': 'overdue_post',
                        'id': post.id,
                    })
        except Exception:
            pass

        # Exported declarations missing exported_date
        decl_sources = [
            ('l10n_be_fiscal_full.models.declaration', 'FiscalDeclaration'),
            ('l10n_be_fiscal_full.models.belcotax', 'BelcotaxDeclaration'),
            ('l10n_lu_fiscal_full.models.declaration', 'FiscalDeclaration'),
        ]
        for module_name, cls_name in decl_sources:
            try:
                module = __import__(module_name, fromlist=[cls_name])
                Cls = getattr(module, cls_name)
            except Exception:
                continue
            for rec in Cls._registry:
                if getattr(rec, 'state', None) == 'exported' and not getattr(rec, 'exported_date', None):
                    issues.append({
                        'model': Cls._name,
                        'issue': 'missing_exported_date',
                        'id': rec.id,
                    })

        return issues
