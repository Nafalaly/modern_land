#  -*- coding: utf-8 -*-
from odoo import models, fields


class ChruchActivityType(models.Model):
    _name = 'church.activity.type'
    _description = 'Chruch Activity Types'

    name = fields.Char(string='Nama')
    report_name = fields.Char(string='Nama Laporan')
    active = fields.Boolean(default=True)
