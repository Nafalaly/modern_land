#  -*- coding: utf-8 -*-
from odoo import models, fields, api


class PengerjaPelayananLine(models.Model):
    _name = 'pengerja.pelayanan.line'
    _description = 'Pelayanan pada pengerja'
    _rec_name = 'display_name'

    display_name = fields.Char(compute='_compute_display_name')
    pengerja_id = fields.Many2one(comodel_name='pengerja', string='Pengerja')
    pelayanan_id = fields.Many2one(comodel_name='bidang.pelayanan', string='Bidang Pelayanan', order='nama_bidang_pelayanan asc')

    _sql_constraints = [
        ('pengerja_pelayanan_uniq', 'unique (pengerja_id,pelayanan_id)', "Pengerja & Pelayanan tidak boleh sama"),
    ]

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = ''
