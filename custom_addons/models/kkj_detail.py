from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class KartuKeluargaJemaat(models.Model):
    _name = 'kartu.keluarga.jemaat.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'kartu keluarga jemaat detail'
    # _rec_name = 'nomor'

    is_jemaat = fields.Boolean(string='Jemaat Gereja', related='nama_jemaat_id.is_jemaat')
    nama_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama Jemaat', required=True, index=True,
                                     default=False)
    tempat_lahir = fields.Char(string='Tempat Lahir', related='nama_jemaat_id.tempat_lahir')
    tanggal_lahir = fields.Date(string='Tanggal Lahir', related='nama_jemaat_id.tanggal_lahir')
    kkj_id = fields.Many2one(comodel_name='kartu.keluarga.jemaat', string='Kartu Keluarga Jemaat', ondelete='cascade')
    sequence = fields.Integer(string='sequence')
    pekerjaan = fields.Selection([
        ('tidak bekerja', 'Tidak Bekerja'),
        ('pegawai negeri', 'Pegawai Negeri'),
        ('pegawai swasta', 'Pegawai Swasta'),
        ('wiraswasta', 'Wiraswasta'),
        ('profesional', 'Profesional'),
        ('abri', 'ABRI'),
        ('hamba tuhan', 'Hamba Tuhan'),
        ('lain-lain', 'Lain-lain'),
    ], 'Pekerjaan', related='nama_jemaat_id.pekerjaan')
    pendidikan = fields.Selection([
        ('tidak sekolah', 'Tidak Sekolah'),
        ('sekolah dasar', 'SD'),
        ('sekolah menengah pertama', 'SMP/SLTP'),
        ('sekolah menengah utama/sekolah menengah kejuruan', 'SLTA/SMU/Sederajat'),
        ('tingkat akademi', 'Tingkat Akademi'),
        ('tingkat universitas', 'Tingkat Universitas/Sarjana'),
    ], 'Pendidikan Terakhir', related='nama_jemaat_id.pendidikan')
    hubungan_keluarga = fields.Selection([
        ('suami', 'Suami'),
        ('istri', 'Istri'),
        ('anak', 'Anak'),
        ('orang tua', 'Orang Tua'),
        ('saudara/family', 'Saudara/Family'),
        ('pembantu', 'Pembantu'),
        ('orang lain', 'Orang Lain'),
        ('cucu', 'Cucu'),
    ], 'Hubungan Keluarga', required=True)

    # Company Address
    parent_id = fields.Many2one(comodel_name='res.partner', string='Nama Perusahaan', help='Tempat Bekerja',
                                related='nama_jemaat_id.parent_id')

    full_address = fields.Char(string='Alamat Perusahaan', related='parent_id.full_address')

    tanggal_terdaftar = fields.Date(string='Tanggal Terdaftar')
    jabatan_gereja = fields.Selection([
        ('jemaat', 'Jemaat'),
        ('aktivis', 'Aktivis'),
        ('pengerja', 'Pengerja'),
        ('gembala cabang/ranting', 'Gembala Cabang/Ranting'),
    ], 'Jabatan Gereja', default="jemaat")
    baptis_roh_kudus = fields.Selection([
        ('sudah', 'Sudah'),
        ('belum', 'Belum'),
    ], 'Baptis Roh Kudus', default="sudah", required=True)

    #diserahkan
    tanggal_penyerahan = fields.Date(string='Tanggal')
    tempat_penyerahan = fields.Char(string='Tempat Gereja')
    pendeta_penyerahan = fields.Char(string='Pendeta yang melayani')

    #baptisan selam
    tanggal_baptis_selam = fields.Date(string='Tanggal')
    tempat_baptis_selam = fields.Char(string='Tempat Gereja')
    pendeta_baptis_selam = fields.Char(string='Pendeta yang melayani')

    #pernikahan
    tanggal_pernikahan = fields.Date(string='Tanggal')
    tempat_pernikahan = fields.Char(string='Tempat Gereja')
    pendeta_pernikahan = fields.Char(string='Pendeta yang melayani')

    #kematian
    tanggal_kematian = fields.Date(string='Tanggal')
    tempat_kematian = fields.Char(string='Gereja yang melayani')
    pendeta_kematian = fields.Char(string='Pendeta yang melayani')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for data in self:
            for detail in data.kkj_id:
                if detail.state not in ('draft', 'cancel'):
                    raise UserError(_(
                        "You can not delete a data."
                        " You must first cancel it."))
