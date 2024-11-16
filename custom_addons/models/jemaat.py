from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class Jemaat(models.Model):
    _name = 'jemaat'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data jemaat'
    _rec_name = 'name'

    nomor = fields.Char('Nomor Jemaat', required=True, index=True, readonly=True, default=lambda self: _('New'))
    name = fields.Char('Nama Jemaat', required=True)
    tempat_lahir = fields.Char(string='Tempat Lahir', required=True)
    tanggal_lahir = fields.Date(string='Tanggal Lahir', required=True)
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('wanita', 'Wanita')
    ], 'Jenis Kelamin')
    pendidikan = fields.Selection([
        ('tidak sekolah', 'Tidak Sekolah'),
        ('sekolah dasar', 'SD'),
        ('sekolah menengah pertama', 'SMP/SLTP'),
        ('sekolah menengah utama/sekolah menengah kejuruan', 'SLTA/SMU/Sederajat'),
        ('tingkat akademi', 'Tingkat Akademi'),
        ('tingkat universitas', 'Tingkat Universitas/Sarjana'),
    ], 'Pendidikan Terakhir', default="tidak sekolah")
    nomor_telpon = fields.Char('Nomor Telpon Rumah/Kantor')
    nomor_hp = fields.Char('Nomor Handphone')
    golongan_darah = fields.Selection([
        ('', ''),
        ('O', 'O'),
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
    ], default='', string='Golongan Darah')
    gereja_id = fields.Many2one(comodel_name='gereja', string='Gereja', ondelete='set null')
    email = fields.Char(string='Email')

    is_baptis = fields.Boolean(string='Sudah dibaptis', default=False)
    is_baptis_roh_kudus = fields.Boolean(string='Sudah dibaptis Roh Kudus', default=False)
    is_ayah_jemaat = fields.Boolean(string='Apakah Ayah Jemaat?', default=False)
    nama_ayah = fields.Char(string='Nama Ayah')
    nama_ayah_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama Ayah')
    is_ibu_jemaat = fields.Boolean(string='Apakah Ibu Jemaat?', default=False)
    nama_ibu = fields.Char(string='Nama Ibu')
    nama_ibu_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama Ibu')

    baptisan_id = fields.Many2one(comodel_name='baptisan', string='Nomor Baptisan', ondelete='set null', default=False)
    kkj_id = fields.Many2one(comodel_name='kartu.keluarga.jemaat', string='Nomor KKJ', ondelete='set null', default=False)

    alamat = fields.Text('Alamat')
    provinsi = fields.Char('Provinsi')
    kota = fields.Char('Kabupaten/Kota')
    kecamatan = fields.Char('Kecamatan')
    kelurahan = fields.Char('Kelurahan/Desa')
    kodepos = fields.Char('Kodepos')

    pengerja_line_id = fields.One2many(comodel_name='pengerja', inverse_name='name_id', string='Nama Jemaat')
    cool_line_id = fields.One2many(comodel_name='cool.anggota', inverse_name='jemaat_id', string='Nama Jemaat')
    cool_doa_line_id = fields.One2many(comodel_name='cool.kubu.doa', inverse_name='jemaat_id', string='Nama Jemaat')

    # rank_name = fields.Char(string='Rank Name')
    image_1920 = fields.Image("Foto Jemaat", max_width=1920, max_height=1920)
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
                    'app.jemaat.seq', sequence_date=seq_date) or _("New")

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

    def approve_jemaat(self):
        self.change_state('approved')

    def redraft_jemaat(self):
        self.change_state('draft')