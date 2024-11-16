from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class Pengerja(models.Model):
    _name = 'pengerja'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data pengerja'
    _rec_name = 'name_id'

    nomor = fields.Char('Nomor', required=True, index=True, readonly=True, default=lambda self: _('New'))
    name_id = fields.Many2one(comodel_name='jemaat', string='Nama Pengerja', required=True)
    kode_badge = fields.Char('Kode Badge')
    bidang_pelayanan1 = fields.Many2one(comodel_name='bidang.pelayanan', string='Bidang Pelayanan 1', order='nama_bidang_pelayanan asc')
    bidang_pelayanan2 = fields.Many2one(comodel_name='bidang.pelayanan', string='Bidang Pelayanan 2', order='nama_bidang_pelayanan asc')
    bidang_pelayanan3 = fields.Many2one(comodel_name='bidang.pelayanan', string='Bidang Pelayanan 3', order='nama_bidang_pelayanan asc')
    is_kkj = fields.Boolean(string='KKJ ?', default=False)
    nomor_kkj = fields.Many2one(comodel_name='kartu.keluarga.jemaat', string='Nomor KKJ')
    is_baptis = fields.Boolean(string='Sudah dibaptis ?', default=False)
    nomor_baptis = fields.Many2one(comodel_name='baptisan', string='Nomor Baptisan')
    is_kom = fields.Boolean(string='Sudah ikut KOM ?', default=False)
    is_formulir_komitmen = fields.Boolean(string='Mengisi Formulir Komitmen ?', default=False)
    is_mdpj_online = fields.Boolean(string='Ikut MDPJ Online ?', default=False)
    mdpj_onsite = fields.Selection([
        ('bersedia', 'Bersedia'),
        ('belum bersedia', 'Belum Bersedia'),
        ('tidak bersedia', 'Tidak Bersedia'),
    ], string='Bersedia ikut MDPJ Onsite ?', default='bersedia')
    image_1920 = fields.Image("Foto Pengerja", max_width=1920, max_height=1920)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

    baptisan_line_ids = fields.One2many(comodel_name='baptisan', inverse_name='nama_pendeta_id', string='Pendeta yang membaptis')
    gereja_line_ids = fields.One2many(comodel_name='gereja', inverse_name='gembala_id', string='Nama Gembala')

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
                    'app.pengerja.seq', sequence_date=seq_date) or _("New")

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

    def approve_pengerja(self):
        self.change_state('approved')

    def redraft_pengerja(self):
        self.change_state('draft')