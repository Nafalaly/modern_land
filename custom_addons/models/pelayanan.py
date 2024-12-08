from odoo import models, fields, _


class BidangPelayanan(models.Model):
    _name = 'bidang.pelayanan'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'data Bidang Pelayanan'
    _rec_name = 'nama_bidang_pelayanan'

    _rec_seq_fields_name = {
        'nomor': 'app.bidang.pelayanan.seq'
    }

    nomor = fields.Char('Nomor Bidang Pelayanan', required=True, index=True, readonly=True,
                        default=lambda self: _('New'))
    nama_bidang_pelayanan = fields.Char(string='Bidang Pelayanan', required=True)
    pelayanan_baptisan = fields.Boolean(string='Pembaptisan', default=False)
    pelayanan_penyerahan_anak = fields.Boolean(string='Penyerahan Anak', default=False)
    pelayanan_pernikahan = fields.Boolean(string='Pemberkatan Nikah', default=False)
    pelayanan_kematian = fields.Boolean(string='Pelayanan Kematian', default=False)
    pelayanan_gembala = fields.Boolean(string='Pelayanan Gembala', default=False)

    # as default Pelayanan will always in confirm state,
    # in case need two ways validation then remove this code
    state = fields.Selection(default="confirm")

