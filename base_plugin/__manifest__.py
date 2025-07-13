{
    'name': 'Base Plugin',
    'version': '16.0.1.0.0',
    'summary': 'Basic plugin structure',
    'description': 'Example skeleton for an Odoo addon.',
    'author': 'Example Author, Thibault Ahn',
    'category': 'Tools',
    'icon': '/base_plugin/static/description/icon.svg',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_model_views.xml',
    ],
    'installable': True,
    'application': False,
}
