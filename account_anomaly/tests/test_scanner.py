import datetime
import importlib


def get_scanner():
    from account_anomaly.models import scanner
    importlib.reload(scanner)
    return scanner.AnomalyScanner


def test_scanner_detects_duplicate_bank(partner_bank_class):
    Bank = partner_bank_class
    b1 = Bank(acc_number='ABC')
    b2 = Bank(acc_number='ABC')

    Scanner = get_scanner()
    issues = Scanner.scan_all()

    assert any(i.get('issue') == 'duplicate_acc_number' and i.get('acc_number') == 'ABC' for i in issues)
    assert any(b1.id in i.get('ids', []) and b2.id in i.get('ids', []) for i in issues)


def test_scanner_detects_overdue_posts(social_post_class, monkeypatch):
    SocialPost = social_post_class
    post = SocialPost(
        name='late',
        account_id=None,
        content='x',
        scheduled_date=datetime.datetime.now() - datetime.timedelta(days=1),
        state='scheduled',
        stats_impressions=0,
        stats_clicks=0,
    )

    monkeypatch.setattr(SocialPost, 'search', lambda self, domain: [post], raising=False)

    Scanner = get_scanner()
    issues = Scanner.scan_all()

    assert any(i.get('issue') == 'overdue_post' and i.get('id') == post.id for i in issues)


def test_scanner_detects_missing_export_date(fiscal_declaration_class, lu_fiscal_declaration_class):
    BEDecl = fiscal_declaration_class
    LUDecl = lu_fiscal_declaration_class

    be = BEDecl(name='BE', declaration_type='vat', state='exported', exported_date=None)
    lu = LUDecl(name='LU', declaration_type='vat', state='exported', exported_date=None)

    Scanner = get_scanner()
    issues = Scanner.scan_all()

    be_issue = any(i.get('model') == BEDecl._name and i.get('issue') == 'missing_exported_date' and i.get('id') == be.id for i in issues)
    lu_issue = any(i.get('model') == LUDecl._name and i.get('issue') == 'missing_exported_date' and i.get('id') == lu.id for i in issues)

    assert be_issue
    assert lu_issue
