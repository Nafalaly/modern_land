from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class BidangPelayanan(models.Model):
    _name = 'bidang.pelayanan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data bidang pelayanan'
    _rec_name = 'nama_bidang_pelayanan'

    nomor = fields.Char('Nomor Bidang Pelayanan', required=True, index=True, readonly=True, default=lambda self: _('New'))
    nama_bidang_pelayanan = fields.Char(string='Bidang Pelayanan', required=True)
    pelayanan_baptisan = fields.Boolean(string='Pembaptisan', default=False)
    pelayanan_penyerahan_anak = fields.Boolean(string='Penyerahan Anak', default=False)
    pelayanan_pernikahan = fields.Boolean(string='Pemberkatan Nikah', default=False)
    pelayanan_kematian = fields.Boolean(string='Pelayanan Kematian', default=False)
    pelayanan_gembala = fields.Boolean(string='Pelayanan Gembala', default=False)
    sequence = fields.Integer(string='Urutan Sequence', compute='_compute_increment', default=1, store=True)

    def _compute_increment(self):
        max_sequence = self.env['bidang.pelayanan'].search([], order='sequence desc', limit=1).sequence
        return max_sequence + 1

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('nomor', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['create_date'])
                ) if 'create_date' in vals else None
                vals['nomor'] = self.env['ir.sequence'].next_by_code(
                    'app.bidang.pelayanan.seq', sequence_date=seq_date) or _("New")

        return super().create(vals_list)