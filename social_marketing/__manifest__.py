{
    'name': 'Social Marketing',
    'version': '16.0.1.0.0',
    'summary': 'Manage social media posts and accounts',
    'description': 'Example module for scheduling posts and tracking basic metrics.',
    'author': 'Example Author',
    'category': 'Marketing',
    'depends': ['base'],
    'data': [
        'security/social_marketing_security.xml',
        'security/ir.model.access.csv',
        'data/scheduled_actions.xml',
        'views/social_account_views.xml',
        'views/social_post_views.xml',
    ],
    'installable': True,
    'application': True,
}
