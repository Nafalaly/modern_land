# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tilabs Cities',
    'version': '1.0',
    'sequence': 10,
    'summary': 'Indonesian Cities',
    'depends': ['base_address_extended','contacts','base'],
    'data': [
        "data/res.city.csv",
        "data/menu.xml"
    ],
    'license': 'LGPL-3',
}