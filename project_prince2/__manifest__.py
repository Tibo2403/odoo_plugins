{
    'name': 'Project PRINCE2',
    'version': '16.0.1.0.0',
    'summary': 'Manage projects using the PRINCE2 methodology',
    'description': 'Example addon implementing a simplified PRINCE2 workflow.',
    'author': 'Example Author, Thibault Ahn',
    'category': 'Project',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/prince2_project_views.xml',
    ],
    'installable': True,
    'application': True,
}
