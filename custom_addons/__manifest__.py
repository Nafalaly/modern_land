# -*- coding: utf-8 -*-
{
    'name': "custom_addons",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Suhardi Siasono",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Apps Gereja',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/baptisan_views.xml',
        'views/pengerja_views.xml',
        'views/gereja_views.xml',
        'views/jemaat_views.xml',
        'views/kkj_views.xml',
        'views/provinsi_views.xml',
        'views/kota_views.xml',
        'views/cool_views.xml',
        'views/penyerahan_anak_views.xml',
        'views/akta_nikah_views.xml',
        'views/bidang_pelayanan_views.xml',
        'views/menu_views.xml',
        'data/sequence.xml',

    ],
    'license': 'LGPL-3',
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
