from odoo import models, fields
from odoo.tools.translate import _

class AktaNikah(models.Model):
    _name = 'akta.nikah'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'Data Akta Nikah'
    _rec_name = 'nomor'

    _rec_seq_fields_name = {
        'nomor': 'app.akta.nikah.seq'
    }

    nomor = fields.Char('Nomor Akta Nikah', required=True, index=True, readonly=True,
                        default=lambda self: _('New'))
    tanggal_konseling = fields.Date(string='Tanggal Konseling', required=True)
    tanggal_pernikahan = fields.Date(string='Tanggal Pernikahan', required=True)
    pendeta_id = fields.Many2one(comodel_name='pengerja', string='Nama Pendeta', required=True)
    pelayanan = fields.Selection([
        ('pernikahan', 'Pernikahan'),
        ('peneguhan', 'Peneguhan')
    ], string='Pelayanan', default='pernikahan', required=True)
    gereja_id = fields.Many2one(comodel_name='gereja', string='Cabang/Ranting', required=True)

    # Suami Informations
    is_suami_jemaat = fields.Boolean(related='suami_jemaat_id.is_jemaat')
    suami_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama', index=True, required=True)
    suami_tempat_lahir = fields.Char(related='suami_jemaat_id.tempat_lahir')
    suami_tanggal_lahir = fields.Date(related='suami_jemaat_id.tanggal_lahir')
    suami_no_ktp = fields.Char(related='suami_jemaat_id.no_ktp')

    suami_alamat = fields.Char(related='suami_jemaat_id.full_address')

    suami_telpon = fields.Char(related='suami_jemaat_id.mobile')
    suami_gereja_id = fields.Many2one(comodel_name='gereja',
                                      related='suami_jemaat_id.gereja_id', string='Baptis di Gereja')
    suami_status_pernikahan = fields.Selection([
        ('belum menikah', 'Belum Menikah'),
        ('pernah menikah', 'Pernah Menikah')
    ], string='Status Pernikahan')

    suami_ayah = fields.Many2one(comodel_name='res.partner', related='suami_jemaat_id.ayah_jemaat_id',
                                 string='Nama Ayah')
    suami_ibu = fields.Many2one(comodel_name='res.partner', related='suami_jemaat_id.ibu_jemaat_id', string='Nama Ibu')

    # File Attachments
    suami_akta_lahir = fields.Binary("Upload Fotocopy Akta Lahir")
    suami_akta_lahir_name = fields.Char(string='Fotocopy Akta Lahir')
    suami_kk_legalisir = fields.Binary("Upload Fotocopy KK Legalisir")
    suami_kk_legalisir_name = fields.Char(string='Fotocopy KK Legalisir')
    suami_baptisan_selam = fields.Binary("Upload Fotocopy Surat Baptisan Selam")
    suami_baptisan_selam_name = fields.Char(string='Fotocopy Surat Baptisan Selam')
    suami_kkj = fields.Binary("Upload Fotocopy KKJ")
    suami_kkj_name = fields.Char(string='Fotocopy KKJ')
    suami_ktp = fields.Binary("Upload Fotocopy KTP")
    suami_ktp_name = fields.Char(string='Fotocopy KTP')
    suami_surat_persetujuan_orang_tua = fields.Binary("Upload Surat Persetujuan Orang Tua (Asli)")
    suami_surat_persetujuan_orang_tua_name = fields.Char(string='Surat Persetujuan Orang Tua (Asli)')
    suami_surat_keterangan_belum_nikah = fields.Binary("Upload Surat Keterangan Belum Nikah (N1-N4)")
    suami_surat_keterangan_belum_nikah_name = fields.Char(string='Surat Keterangan Belum Nikah (N1-N4)')
    suami_surat_sertifikat_kom_100 = fields.Binary("Upload Fotocopy Sertifikat KOM seri 100")
    suami_surat_sertifikat_kom_100_name = fields.Char(string='Fotocopy Sertifikat KOM seri 100')
    suami_formulir_asli = fields.Binary("Upload Formulir Asli")
    suami_formulir_asli_name = fields.Char(string='Formulir Asli')
    suami_pasfoto = fields.Binary("Upload Pas foto bersama uk.6x4 (berwarna 3 lbr)")
    suami_pasfoto_name = fields.Char(string='Pas foto bersama uk.6x4 (berwarna 3 lbr)')

    is_istri_jemaat = fields.Boolean(related='istri_jemaat_id.is_jemaat')
    istri_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama', index=True, required=True)
    istri_tempat_lahir = fields.Char(related='istri_jemaat_id.tempat_lahir')
    istri_tanggal_lahir = fields.Date(related='istri_jemaat_id.tanggal_lahir')
    istri_no_ktp = fields.Char(related='istri_jemaat_id.no_ktp')
    istri_alamat = fields.Char(related='istri_jemaat_id.full_address')
    istri_telpon = fields.Char(related='istri_jemaat_id.mobile')
    istri_gereja_id = fields.Many2one(comodel_name='gereja',
                                      related='istri_jemaat_id.gereja_id', string='Baptis di Gereja')
    istri_status_pernikahan = fields.Selection([
        ('belum menikah', 'Belum Menikah'),
        ('pernah menikah', 'Pernah Menikah')
    ], string='Status Pernikahan')

    istri_ayah = fields.Many2one(comodel_name='res.partner', related='istri_jemaat_id.ayah_jemaat_id',
                                 string='Nama Ayah')
    istri_ibu = fields.Many2one(comodel_name='res.partner', related='istri_jemaat_id.ibu_jemaat_id', string='Nama Ibu')

    istri_akta_lahir = fields.Binary("Upload Fotocopy Akta Lahir")
    istri_akta_lahir_name = fields.Char(string='Fotocopy Akta Lahir')
    istri_kk_legalisir = fields.Binary("Upload Fotocopy KK Legalisir")
    istri_kk_legalisir_name = fields.Char(string='Fotocopy KK Legalisir')
    istri_baptisan_selam = fields.Binary("Upload Fotocopy Surat Baptisan Selam")
    istri_baptisan_selam_name = fields.Char(string='Fotocopy Surat Baptisan Selam')
    istri_kkj = fields.Binary("Upload Fotocopy KKJ")
    istri_kkj_name = fields.Char(string='Fotocopy KKJ')
    istri_ktp = fields.Binary("Upload Fotocopy KTP")
    istri_ktp_name = fields.Char(string='Fotocopy KTP')
    istri_surat_persetujuan_orang_tua = fields.Binary("Upload Surat Persetujuan Orang Tua (Asli)")
    istri_surat_persetujuan_orang_tua_name = fields.Char(string='Surat Persetujuan Orang Tua (Asli)')
    istri_surat_keterangan_belum_nikah = fields.Binary("Upload Surat Keterangan Belum Nikah (N1-N4)")
    istri_surat_keterangan_belum_nikah_name = fields.Char(string='Surat Keterangan Belum Nikah (N1-N4)')
    istri_surat_sertifikat_kom_100 = fields.Binary("Upload Fotocopy Sertifikat KOM seri 100")
    istri_surat_sertifikat_kom_100_name = fields.Char(string='Fotocopy Sertifikat KOM seri 100')
    istri_formulir_asli = fields.Binary("Upload Formulir Asli")
    istri_formulir_asli_name = fields.Char(string='Formulir Asli')
    istri_pasfoto = fields.Binary("Upload Pas foto bersama uk.6x4 (berwarna 3 lbr)")
    istri_pasfoto_name = fields.Char(string='Pas foto bersama uk.6x4 (berwarna 3 lbr)')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], 'Status', default="draft")

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]
