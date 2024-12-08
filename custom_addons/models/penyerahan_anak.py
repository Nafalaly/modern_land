from odoo import models, fields
from odoo.tools.translate import _


class PenyerahanAnak(models.Model):
    _name = 'penyerahan.anak'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'Data Penyerahan Anak'
    _rec_name = 'nomor'

    _rec_seq_fields_name = {
        'nomor': 'app.peny.anak.seq'
    }

    nomor = fields.Char('Nomor Penyerahan Anak', required=True, index=True, readonly=True,
                        default=lambda self: _('New'))
    gereja_id = fields.Many2one(comodel_name='gereja', string='Gereja', ondelete='set null')
    nama_anak = fields.Char(string='Nama Anak', required=True)
    tempat_lahir = fields.Char(string='Tempat Lahir', required=True)
    tanggal_lahir = fields.Date(string='Tanggal Lahir', required=True)
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('wanita', 'Wanita')
    ], 'Jenis Kelamin')
    partner_id = fields.Many2one(comodel_name='res.partner', help='Related Jemaat')
    tanggal_penyerahan = fields.Date(string='Tanggal Penyerahan', required=True)
    nama_pendeta_id = fields.Many2one(comodel_name='pengerja', string='Nama Pendeta', ondelete='set null')
    image_1920 = fields.Image("Foto", max_width=1920, max_height=1920)
    is_ayah_jemaat = fields.Boolean(string='Ayah Jemaat ?', related='nama_ayah_jemaat_id.is_jemaat')
    nama_ayah_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama Ayah', domain=[('is_jemaat', '=', True)],
                                          ondelete='set null')
    is_ibu_jemaat = fields.Boolean(string='Ibu Jemaat ?', related='nama_ibu_jemaat_id.is_jemaat')
    nama_ibu_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama Ibu', ondelete='set null')

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]
