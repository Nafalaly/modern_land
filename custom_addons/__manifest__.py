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
    'category': 'Apps Gereja',
    'version': '0.1',
    'application': True,
    'depends': ['base', 'mail', 'base_address_extended', 'field_timepicker'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
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
        'views/chruch_activity_type.xml',
        'views/menu_views.xml',
        'data/sequence.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_addons/static/src/scss/style.scss',
        ],
    },
    'license': 'LGPL-3',
}
