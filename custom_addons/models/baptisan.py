from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class Baptisan(models.Model):
    _name = 'baptisan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data baptisan'
    _rec_name = 'nama_jemaat_id'

    nomor = fields.Char('Nomor Baptisan', required=True, index=True, readonly=True, default=lambda self: _('New'))
    nama_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama Jemaat', required=True, index=True)
    nama_pendeta_id = fields.Many2one(comodel_name='pengerja', string='Pendeta yang membaptis', domain="[('state', '=', 'approved'), '|', '|', ('bidang_pelayanan1.pelayanan_gembala', '=', True), ('bidang_pelayanan2.pelayanan_gembala', '=', True), ('bidang_pelayanan3.pelayanan_gembala', '=', True)]")
    tempat_baptis = fields.Char(string='Tempat Baptis')
    tanggal_baptis = fields.Date(string='Tanggal Baptis')
    gereja_id = fields.Many2one(comodel_name='gereja', string='Nama Gereja', ondelete='set null')
    image_1920 = fields.Image("Foto Baptisan", max_width=1920, max_height=1920)
    jemaat_ids = fields.One2many(comodel_name='jemaat', inverse_name='baptisan_id', string='Jemaat')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

    pengerja_line_ids = fields.One2many(comodel_name='pengerja', inverse_name='nomor_baptis', string='Pengerja')

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
                    'app.baptisan.seq', sequence_date=seq_date) or _("New")

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


    def approve_baptisan(self):
        self.change_state('approved')

    def redraft_baptisan(self):
        self.change_state('draft')