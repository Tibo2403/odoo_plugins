{
    'name': 'Social Marketing',
    'version': '16.0.1.0.0',
    'summary': 'Schedule and track social media posts',
    'description': 'Example addon for managing social accounts, scheduled posts, and basic engagement metrics.',
    'author': 'Example Author, Thibault Ahn',
    'category': 'Marketing',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/scheduled_actions.xml',
        'views/social_marketing_views.xml',
    ],
    'installable': True,
    'application': True,
}
