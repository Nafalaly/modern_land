from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class Pengerja(models.Model):
    _name = 'pengerja'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data pengerja/Gembala'
    _rec_name = 'display_name'

    def _compute_display_name(self):
        for rec in self:
            badge = '- ' + rec.kode_badge if rec.kode_badge else ''
            rec.display_name = f"{rec.partner_id.name} {badge}"

    display_name = fields.Char(help='Display Pengerja', compute='_compute_display_name')
    nomor = fields.Char('Nomor', required=True, index=True, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one(comodel_name='res.partner', string='Nama Pengerja', required=True)
    kode_badge = fields.Char('Kode Badge')
    pelayanan_line = fields.One2many(comodel_name='pengerja.pelayanan.line', inverse_name='pengerja_id',
                                     string='Pelayanan')
    is_kkj = fields.Boolean(string='KKJ ?', default=False)
    nomor_kkj = fields.Many2one(comodel_name='kartu.keluarga.jemaat', string='Nomor KKJ')
    is_baptis = fields.Boolean(string='Sudah dibaptis ?', related='partner_id.is_baptis')
    nomor_baptis = fields.Many2one(comodel_name='baptisan', string='Nomor Baptisan')
    is_kom = fields.Boolean(string='Sudah ikut KOM ?', default=False)
    is_formulir_komitmen = fields.Boolean(string='Mengisi Formulir Komitmen ?', default=False)
    is_mdpj_online = fields.Boolean(string='Ikut MDPJ Online ?', default=False)
    mdpj_onsite = fields.Selection([
        ('bersedia', 'Bersedia'),
        ('belum bersedia', 'Belum Bersedia'),
        ('tidak bersedia', 'Tidak Bersedia'),
    ], string='Bersedia ikut MDPJ Onsite ?', default='bersedia')
    image_1920 = fields.Image("Foto Pengerja", related='partner_id.image_1920')
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