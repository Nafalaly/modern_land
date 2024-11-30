#  -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Jemaat(models.Model):
    """
    Inherit res.partner
    to full fill Jemaat base information's
    """
    _inherit = 'res.partner'

    is_jemaat = fields.Boolean(string='Jemaat', help='True if Partner is Jemaat')
    jemaat_number = fields.Char('Nomor Jemaat', required=True, index=True, readonly=True,
                                default=lambda self: _('New'), tracking=True)
    tanggal_lahir = fields.Date(string='Tanggal Lahir', required=True)
    tempat_lahir = fields.Char(string='Tempat Lahir', required=True)
    jenis_kelamin = fields.Selection([
        ('male', 'Laki-Laki'),
        ('female', 'Wanita')
    ], 'Jenis Kelamin', required=True)

    @api.onchange('pekerjaan')
    def onchange_pekerjaan(self):
        """
        Method to copy value from pekerjaan to default 'function' field in
        res.partner
        """
        for rec in self:
            if rec.pekerjaan not in ['tidak bekerja', 'lain-lain']:
                rec.function = rec.pekerjaan
    # TODO: Create Umur computed (?)

    pekerjaan = fields.Selection([
        ('tidak bekerja', 'Tidak Bekerja'),
        ('pegawai negeri', 'Pegawai Negeri'),
        ('pegawai swasta', 'Pegawai Swasta'),
        ('wiraswasta', 'Wiraswasta'),
        ('profesional', 'Profesional'),
        ('abri', 'ABRI'),
        ('hamba tuhan', 'Hamba Tuhan'),
        ('lain-lain', 'Lain-lain'),
    ], 'Pekerjaan', default="tidak bekerja")
    pendidikan = fields.Selection([
        ('tidak sekolah', 'Tidak Sekolah'),
        ('sekolah dasar', 'SD'),
        ('sekolah menengah pertama', 'SMP/SLTP'),
        ('sekolah menengah utama/sekolah menengah kejuruan', 'SLTA/SMU/Sederajat'),
        ('tingkat akademi', 'Tingkat Akademi'),
        ('tingkat universitas', 'Tingkat Universitas/Sarjana'),
    ], 'Pendidikan Terakhir', default="tidak sekolah", tracking=True)
    golongan_darah = fields.Selection([
        ('O', 'O'),
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
    ], string='Golongan Darah')
    gereja_id = fields.Many2one(comodel_name='gereja', string='Gereja', ondelete='restrict', index=True, required=True,
                                tracking=True)
    is_baptis = fields.Boolean(string='Sudah dibaptis', default=False)
    is_baptis_roh_kudus = fields.Boolean(string='Sudah dibaptis Roh Kudus', default=False)
    is_ayah_jemaat = fields.Boolean(string='Apakah Ayah Jemaat?', related='ayah_jemaat_id.is_jemaat')
    ayah_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Ayah', tracking=True)
    ibu_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Ibu', tracking=True)
    is_ibu_jemaat = fields.Boolean(string='Apakah Ibu Jemaat?', related='ibu_jemaat_id.is_jemaat')

    baptisan_id = fields.Many2one(comodel_name='baptisan', string='Nomor Baptisan', ondelete='set null', default=False)
    kkj_id = fields.Many2one(comodel_name='kartu.keluarga.jemaat', string='Nomor KKJ', ondelete='set null',
                             default=False)

    pengerja_line_id = fields.One2many(comodel_name='pengerja', inverse_name='partner_id', string='Nama Jemaat')
    pengerja_count = fields.Float(compute='_compute_pengerja_count')
    cool_line_id = fields.One2many(comodel_name='cool.anggota', inverse_name='jemaat_id', string='Nama Jemaat')
    cool_doa_line_id = fields.One2many(comodel_name='cool.kubu.doa', inverse_name='jemaat_id', string='Nama Jemaat')

    _sql_constraints = [
        ('nomor_uniq', 'unique (jemaat_number)', "Jemaat Number already exists !"),
    ]

    def _compute_pengerja_count(self):
        self.pengerja_count = len(self.pengerja_line_id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('jemaat_number', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['create_date'])
                ) if 'create_date' in vals else None
                vals['jemaat_number'] = self.env['ir.sequence'].next_by_code(
                    'app.jemaat.seq', sequence_date=seq_date) or _("New")

        return super().create(vals_list)

    def _prepare_pengerja_vals(self):
        return {
            'partner_id': self.id,
        }

    @api.model
    def _action_create_pengerja(self):
        self.ensure_one()
        vals = self._prepare_pengerja_vals()
        return self.env['pengerja'].create(vals)

    def action_create_pengerja(self):
        if not self.pengerja_line_id:
            pengerja_id = self._action_create_pengerja()
            action = self.env["ir.actions.actions"]._for_xml_id("custom_addons.pengerja_action")
            action.update({
                'views': [[self.env.ref('custom_addons.pengerja_view_form').id, 'form']],
                'view_mode': 'form',
                'target': 'current',
                'res_id': pengerja_id.id,
            })
            return action
        return False
