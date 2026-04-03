# -*- coding: utf-8 -*-

{
    'name': 'Finance Dashboard',
    'version': '1.0',
    'author': 'Zorvyn',
    'category': 'Finance',
    'license': 'LGPL-3',
    'summary': 'Finance Dashboard System',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/finance_security.xml',
        'views/finance_menu_and_action.xml',
        'views/finance_record_view.xml',
        ],
    'assets': {
        'web.assets_backend': [
            'finance_dashboard_system/static/src/components/finance_dashboard.js',
            'finance_dashboard_system/static/src/components/finance_dashboard.xml',
            'finance_dashboard_system/static/src/components/finance_dashboard.scss',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },
    'installable': True,
    'application': True,
}