#  -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class Jemaat(models.Model):
    """
    Inherit res.partner
    to fulfill Jemaat base information's
    """
    _name = 'res.partner'
    _inherit = ['res.partner', 'gbi.base.document']

    _rec_seq_fields_name = {
        'jemaat_number': 'app.jemaat.seq'
    }

    is_jemaat = fields.Boolean(string='Jemaat', help='True if Partner is Jemaat')
    no_ktp = fields.Char(string='No KTP')
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
    is_baptis = fields.Boolean(string='Sudah dibaptis', compute='_compute_baptisan')
    is_baptis_roh_kudus = fields.Boolean(string='Sudah dibaptis Roh Kudus', default=False)
    is_ayah_jemaat = fields.Boolean(string='Apakah Ayah Jemaat?', related='ayah_jemaat_id.is_jemaat')
    ayah_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Ayah', tracking=True,
                                     domain=[('company_type', '=', 'person')])
    ibu_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Ibu', tracking=True,
                                    domain=[('company_type', '=', 'person')])
    is_ibu_jemaat = fields.Boolean(string='Apakah Ibu Jemaat?', related='ibu_jemaat_id.is_jemaat')

    baptisan_id = fields.Many2one(comodel_name='baptisan', string='Nomor Baptisan', compute='_compute_baptisan')
    kkj_id = fields.Many2one(comodel_name='kartu.keluarga.jemaat', string='Nomor KKJ', ondelete='set null',
                             default=False)

    pengerja_id = fields.Many2one(comodel_name='pengerja', string='Pengerja', compute='_compute_pengerja')
    cool_line_id = fields.One2many(comodel_name='cool.anggota', inverse_name='jemaat_id', string='Nama Jemaat')
    cool_doa_line_id = fields.One2many(comodel_name='cool.kubu.doa', inverse_name='jemaat_id', string='Nama Jemaat')

    # Address Information
    full_address = fields.Char(string='Alamat', help='display the full address',
                               compute='_compute_address')

    def _compute_pengerja(self):
        pengerja_records = self.env['pengerja'].search([('partner_id', 'in', self.ids), ('state', '=', 'confirm')])

        pengerja_map = {p.partner_id.id: p for p in pengerja_records}
        for rec in self:
            pengerja = pengerja_map.get(rec.id, False)
            rec.pengerja_id = pengerja.id if pengerja else False

    def _compute_baptisan(self):
        # Fetch single query
        baptisan_records = self.env['baptisan'].search([('nama_jemaat_id', 'in', self.ids), ('state', '=', 'confirm')])

        baptism_map = {b.nama_jemaat_id.id: b for b in baptisan_records}
        for rec in self:
            baptisan = baptism_map.get(rec.id, False)
            rec.baptisan_id = baptisan.id if baptisan else False
            rec.is_baptis = bool(baptisan)

    def _compute_address(self):
        for rec in self:
            state = rec.state_id.name if rec.state_id else ''
            country = rec.country_id.name if rec.country_id else ''
            rec.full_address = f"""
                    {rec.street} {rec.street2}, {rec.city}, {state}, {country} {rec.zip}
                """

    _sql_constraints = [
        ('nomor_uniq', 'unique (jemaat_number)', "Jemaat Number already exists !"),
    ]

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
        if not self.baptisan_id:
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

    def action_open_pengerja(self):
        if self.pengerja_id:
            action = self.env["ir.actions.actions"]._for_xml_id("custom_addons.pengerja_action")
            action.update({
                'views': [[self.env.ref('custom_addons.pengerja_view_form').id, 'form']],
                'view_mode': 'form',
                'target': 'current',
                'res_id': self.pengerja_id.id,
            })
            return action
        return False

    def action_open_baptis(self):
        if self.baptisan_id:
            action = self.env["ir.actions.actions"]._for_xml_id("custom_addons.baptisan_action")
            action.update({
                'views': [[self.env.ref('custom_addons.baptisan_view_form').id, 'form']],
                'view_mode': 'form',
                'target': 'current',
                'res_id': self.baptisan_id.id,
            })
            return action
        return False
