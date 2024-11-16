from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class Kota(models.Model):
    _name = 'kota'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data kota'

    name = fields.Char('Nama Kota')
    kecamatan_ids = fields.One2many(comodel_name='kecamatan', inverse_name='kota_id', string='Kota')
    provinsi_id = fields.Many2one(comodel_name='provinsi', string='Provinsi', ondelete='set null')
    state = fields.Selection([
        ('active', 'Active'),
        ('not active', 'Not Active'),
    ], 'Status', default="active")

    def action_cancel(self):
        self.change_state('not active')