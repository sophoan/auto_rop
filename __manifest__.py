# -*- coding: utf-8 -*-
{
    'name': "Auto ROP",

    'summary': """
        Dynamically calculate ROP""",

    'description': """
        This module adds a feature to do the auto calculation of Min Qty. of the products based on completed purchases and sales.
    """,

    'author': "Sophooan Sok",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/auto_rop_views.xml',
        'views/order_point_views.xml',
        'data/rop_data.xml',
        'wizard/auto_rop_scheduler_compute_view.xml',
        'views/product_views.xml',
        # 'views/res_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'depends': [
        'product',
        'stock',
        'sale',
        'purchase',
    ],
    'application': True,
    'installable': True,
}