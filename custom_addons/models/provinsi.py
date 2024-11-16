from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class Provinsi(models.Model):
    _name = 'provinsi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data provinsi'

    name = fields.Char('Nama Provinsi')
    kota_ids = fields.One2many(comodel_name='kota', inverse_name='provinsi_id', string='Kota')
    state = fields.Selection([
        ('active', 'Active'),
        ('not active', 'Not Active'),
    ], 'Status', default="active")

    def action_cancel(self):
        self.change_state('not active')