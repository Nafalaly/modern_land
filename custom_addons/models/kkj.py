from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class KartuKeluargaJemaat(models.Model):
    _name = 'kartu.keluarga.jemaat'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'kartu keluarga jemaat'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor KKJ', required=True, index=True, readonly=True, default=lambda self: _('New'))
    nama_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama Jemaat', domain=[('is_jemaat', '=', True)]
                                     , required=True, index=True)
    gereja_id = fields.Many2one(comodel_name='gereja', string='Nama Gereja', ondelete='set null')
    cool_id = fields.Many2one(comodel_name='cool', string='Cool (Jika ada)', default=False)
    image_1920 = fields.Image("Foto KKJ", max_width=1920, max_height=1920)
    nama_darurat = fields.Char(string='Nama')
    alamat_darurat = fields.Text(string='Alamat')
    telpon_darurat = fields.Char(string='Nomo Telpon')
    kkj_detail_line = fields.One2many(comodel_name='kartu.keluarga.jemaat.line', inverse_name='kkj_id',
                                      string='Data Keluarga')
    jemaat_ids = fields.One2many(comodel_name='res.partner', inverse_name='kkj_id', string='Data Jemaat')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

    pengerja_line_ids = fields.One2many(comodel_name='pengerja', inverse_name='nomor_kkj', string='Pengerja')

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
                    'app.kkj.seq', sequence_date=seq_date) or _("New")

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

    def approve_kkj(self):
        self.change_state('approved')

    def redraft_kkj(self):
        self.change_state('draft')
