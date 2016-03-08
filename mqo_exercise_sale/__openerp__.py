# -*- coding: utf-8 -*-
{
    'name': "MQO Exercise Sale",

    'summary': """Manage exercise sales""",

    'description': """
        MQO module for managing exercise sales:
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mqo_exercises', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'templates/templates.xml',
        'views/product.xml',
        #'views/session_workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}