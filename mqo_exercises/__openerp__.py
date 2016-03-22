# -*- coding: utf-8 -*-
{
    'name': "MQO Exercises",

    'summary': """Manage exercises""",

    'description': """
        MQO module for managing exercises:
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'mqo_learner', 'mqo_survey'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'templates/templates.xml',
        'views/allocations.xml',
        'views/assignments.xml',
        'views/bundle.xml',
        'views/bundle_allocations.xml',
        'views/exercises.xml',
        # 'views/learner.xml',
        #'views/session_workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}