from odoo import models, tools, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from odoo.modules.module import get_resource_path, get_manifest
import logging
import base64


_logger = logging.getLogger(__name__)

class Gereja(models.Model):
    _name = 'gereja'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data gereja'
    _rec_name = 'name'

    nomor = fields.Char('Nomor Gereja', required=True, index=True, readonly=True, default=lambda self: _('New'))
    name = fields.Char('Nama Gereja', required=True)
    gembala_id = fields.Many2one(comodel_name='pengerja', string='Nama Gembala', ondelete='restrict')
    rank_id = fields.Many2one(comodel_name='rank', string='Rank Gereja', ondelete='restrict')

    alamat = fields.Text('Alamat')
    provinsi = fields.Char('Provinsi')
    kota = fields.Char ('Kabupaten/Kota')
    kecamatan = fields.Char('Kecamatan')
    kelurahan = fields.Char('Kelurahan/Desa')
    kodepos = fields.Char('Kodepos')
    nomor_telpon = fields.Char('Nomor Telpon')

    parent_id = fields.Many2one(comodel_name='gereja', string='Cabang/Ranting Dari', ondelete='set null')
    # is_cabang = fields.Boolean(string="Memiliki cabang/ranting", help="Bila Gereja memiliki cabang/ranting, silakan berikan tanda", default=False)

    jemaat_line_id = fields.One2many(comodel_name='jemaat', inverse_name='gereja_id', string='Jemaat')
    cool_line_id = fields.One2many(comodel_name='cool', inverse_name='gereja_id', string='Cool')

    image_1920 = fields.Image("Foto Gereja", max_width=1920, max_height=1920)
    # rayon = fields.Selection([
    #     ('', ''),
    #     ('induk', 'Induk'),
    #     ('rayon', 'Rayon'),
    #     ('sub rayon', 'Sub Rayon'),
    # ], 'Rayon', default="")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
        ('name_uniq', 'unique (name)', "nama already exists !"),
    ]

    # kelurahan = fields.Many2one(comodel_name='kelurahan', string='Kelurahan')
    # kecamatan = fields.Many2one(comodel_name='kecamatan', string='Kecamatan')
    # kodepos = fields.Many2one(comodel_name='kodepos', string='Kodepos')

    # @api.constrains('gembala')
    # def _check_gembala(self):
    #     for rec in self:
    #         check_gembala = self.env['gembala'].search([('id', '=', rec.gembala.id)])
    #
    #         if not(check_gembala):
    #             raise ValidationError(_("Please select gembala before"))
    #
    # @api.constrains('cabang')
    # def _check_cabang(self):
    #     for rec in self:
    #         check_cabang = self.env['gereja'].search([('id', '=', rec.cabang.id)])
    #
    #         if not(check_cabang):
    #             raise ValidationError(_("Please select cabang before"))

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
                    'app.gereja.seq', sequence_date=seq_date) or _("New")

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
                   ('approved', 'draft')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for data in self:
            if data.is_allowed_transition(data.state, new_state):
                data.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (data.state, new_state)
                raise UserError(msg)

    def approve_gereja(self):
        self.change_state('approved')

    def redraft_gereja(self):
        self.change_state('draft')