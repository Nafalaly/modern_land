from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class PenyerahanAnak(models.Model):
    _name = 'penyerahan.anak'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'informasi mengenai penyerahan anak'
    _rec_name = 'nomor'

    nomor = fields.Char('Nomor Penyerahan Anak', required=True, index=True, readonly=True, default=lambda self: _('New'))
    gereja_id = fields.Many2one(comodel_name='gereja', string='Gereja', ondelete='set null')
    nama_anak = fields.Char(string='Nama Anak', required=True)
    tempat_lahir = fields.Char(string='Tempat Lahir', required=True)
    tanggal_lahir = fields.Date(string='Tanggal Lahir', required=True)
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('wanita', 'Wanita')
    ], 'Jenis Kelamin')
    tanggal_penyerahan = fields.Date(string='Tanggal Penyerahan', required=True)
    nama_pendeta_id = fields.Many2one(comodel_name='pengerja', string='Nama Pendeta', ondelete='set null')
    image_1920 = fields.Image("Foto", max_width=1920, max_height=1920)
    is_ayah_jemaat = fields.Boolean(string='Ayah Jemaat ?')
    nama_ayah = fields.Char(string='Nama Ayah')
    nama_ayah_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama Ayah', ondelete='set null')
    is_ibu_jemaat = fields.Boolean(string='Ibu Jemaat ?')
    nama_ibu = fields.Char(string='Nama Ibu')
    nama_ibu_jemaat_id = fields.Many2one(comodel_name='jemaat', string='Nama Ibu', ondelete='set null')
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
                    'app.peny.anak.seq', sequence_date=seq_date) or _("New")

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

    def approve_penyerahan_anak(self):
        self.change_state('approved')

    def redraft_penyerahan_anak(self):
        self.change_state('draft')