from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class AktaNikah(models.Model):
    _name = 'akta.nikah'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'informasi mengenai akta nikah'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor Akta Nikah', required=True, index=True, readonly=True,
                        default=lambda self: _('New'))
    tanggal_konseling = fields.Date(string='Tanggal Konseling')
    tanggal_pernikahan = fields.Date(string='Tanggal Pernikahan')
    pendeta_id = fields.Many2one(comodel_name='pengerja', string='Nama Pendeta')
    pelayanan = fields.Selection([
        ('pernikahan', 'Pernikahan'),
        ('peneguhan', 'Peneguhan')
    ], string='Pelayanan')
    gereja_id = fields.Many2one(comodel_name='gereja', string='Cabang/Ranting')

    is_suami_jemaat = fields.Boolean(string='Apakah Jemaat ?')
    suami_nama = fields.Char(string='Nama')
    suami_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama', index=True)
    suami_tempat_lahir = fields.Char(string='Tempat Lahir')
    suami_tanggal_lahir = fields.Date(string='Tanggal Lahir')
    suami_no_ktp = fields.Char(string='No. KTP')
    suami_alamat = fields.Text(string='Alamat')
    suami_telpon = fields.Char(string='No. Telpon')
    suami_gereja_id = fields.Many2one(comodel_name='gereja', string='Baptis di Gereja')
    suami_status_pernikahan = fields.Selection([
        ('belum menikah', 'Belum Menikah'),
        ('pernah menikah', 'Pernah Menikah')
    ], string='Status Pernikahan')
    suami_nama_ayah = fields.Char(string='Nama Ayah')
    suami_nama_ibu = fields.Char(string='Nama Ibu')
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

    is_istri_jemaat = fields.Boolean(string='Apakah Jemaat ?')
    istri_nama = fields.Char(string='Nama')
    istri_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama', index=True)
    istri_tempat_lahir = fields.Char(string='Tempat Lahir')
    istri_tanggal_lahir = fields.Date(string='Tanggal Lahir')
    istri_no_ktp = fields.Char(string='No. KTP')
    istri_alamat = fields.Text(string='Alamat')
    istri_telpon = fields.Char(string='No. Telpon')
    istri_gereja_id = fields.Many2one(comodel_name='gereja', string='Baptis di Gereja')
    istri_status_pernikahan = fields.Selection([
        ('belum menikah', 'Belum Menikah'),
        ('pernah menikah', 'Pernah Menikah')
    ], string='Status Pernikahan')
    istri_nama_ayah = fields.Char(string='Nama Ayah')
    istri_nama_ibu = fields.Char(string='Nama Ibu')
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
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

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
                    'app.akta.nikah.seq', sequence_date=seq_date) or _("New")

        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for data in self:
            if data.state not in ('draft', 'cancel'):
                raise UserError(_(
                    "You can not delete a data."
                    " You must first cancel it."))

    def action_cancel(self):
        self.change_state('cancel')

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'approved'),
                   ('approved', 'draft'),
                   ('approved', 'cancel')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for data in self:
            if data.is_allowed_transition(data.state, new_state):
                data.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (data.state, new_state)
                raise UserError(msg)

    def approve_akta_nikah(self):
        self.change_state('approved')

    def redraft_akta_nikah(self):
        self.change_state('draft')