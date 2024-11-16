from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class Kelurahan(models.Model):
    _name = 'kelurahan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data kelurahan'

    name = fields.Char('Nama Kelurahan')
    kodepos = fields.Char('Kodepos')
    kecamatan_id = fields.Many2one(comodel_name='kecamatan', string='Kecamatan', ondelete='set null')
    state = fields.Selection([
        ('active', 'Active'),
        ('not active', 'Not Active'),
    ], 'Status', default="active")

    def action_cancel(self):
        self.change_state('not active')