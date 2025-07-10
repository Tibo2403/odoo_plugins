{
    'name': 'Belgian Fiscal Declarations',
    'version': '16.0.1.0.0',
    'summary': 'Generate Belgian fiscal reports and exports',
    'description': 'Skeleton module for Belgian fiscal declarations (TVA, Belcotax, ISOC, BNB).',
    'author': 'Example Author',
    'category': 'Accounting',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/belcotax_views.xml',
    ],
    'installable': True,
    'application': True,
}
