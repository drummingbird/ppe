# -*- coding: utf-8 -*-
{
    'name': "MQO Website",

    'summary': """Add MQO website extras""",

    'description': """
        MQO module to add extra features to the website:
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'templates/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}