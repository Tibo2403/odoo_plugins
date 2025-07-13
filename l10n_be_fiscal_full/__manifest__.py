{
    'name': 'Belgian Fiscal Declarations',
    'version': '16.0.1.0.0',
    'summary': 'Generate Belgian fiscal reports and exports',
    'description': 'Skeleton module for Belgian fiscal declarations (TVA, Belcotax, ISOC, BNB).',
    'author': 'Example Author, Thibault Ahn',
    'category': 'Accounting',
    'icon': '/l10n_be_fiscal_full/static/description/icon.svg',
    'depends': ['base'],
    'data': [
        'views/belcotax_wizard_views.xml',
        'views/bnb_xbrl_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
}

