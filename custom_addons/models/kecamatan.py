from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class Kecamatan(models.Model):
    _name = 'kecamatan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data kecamatan'

    name = fields.Char('Nama Kecamatan')
    kelurahan_ids = fields.One2many(comodel_name='kelurahan', inverse_name='kecamatan_id', string='Kelurahan')
    kota_id = fields.Many2one(comodel_name='kota', string='Kota', ondelete='set null')
    state = fields.Selection([
        ('active', 'Active'),
        ('not active', 'Not Active'),
    ], 'Status', default="active")

    def action_cancel(self):
        self.change_state('not active')