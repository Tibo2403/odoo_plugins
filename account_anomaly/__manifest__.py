{
    'name': 'Accounting Anomaly',
    'version': '16.0.1.0.0',
    'summary': 'Analyze accounting moves for anomalies',
    'description': 'Simple tools to detect unusual accounting entries.',
    'author': 'Example Author, Thibault Ahn',
    'category': 'Accounting',
    'icon': '/account_anomaly/static/description/icon.svg',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
}
