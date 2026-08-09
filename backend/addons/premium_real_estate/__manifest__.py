{
    'name': 'Premium Real Estate API',
    'version': '1.0',
    'summary': 'Backend API para la aplicación Svelte',
    'category': 'Sales/CRM',
    'author': 'Premium RE',
    'depends': ['base', 'mail', 'crm'],
'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/property_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}