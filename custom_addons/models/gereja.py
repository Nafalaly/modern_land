#  -*- coding: utf-8 -*-
#  -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class Gereja(models.Model):
    _name = 'gereja'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data gereja'
    _rec_name = 'name'

    sequence = fields.Char('Nomor Gereja', index=True, readonly=True, help='No Urut')
    name = fields.Char('Nama Gereja', required=True)
    gembala_id = fields.Many2one(comodel_name='pengerja', string='Nama Gembala', ondelete='restrict')
    rank_id = fields.Many2one(comodel_name='rank', string='Rank Gereja', ondelete='restrict')

    def _get_default_country_id(self):
        """
        Default country_id : Indonesia
        """
        return self.env.ref('base.id')

    def _get_default_state_id(self):
        """
        Default state_id : Jawa Barat
        """
        return self.env.ref('base.state_id_jb')

    # Address Info

    street = fields.Char(string='Street')
    zip = fields.Char(string="Zip Code")
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country', default=_get_default_country_id)
    city_id = fields.Many2one(comodel_name='res.city', string='City ID')
    country_enforce_cities = fields.Boolean(related='country_id.enforce_cities')
    state_id = fields.Many2one("res.country.state", string='State', default=_get_default_state_id)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    full_address = fields.Char(string='Alamat', help='Help to search full address', compute='_compute_address', store=True)

    # Operational Schedule
    operational_schedule_line = fields.One2many(comodel_name='chruch.operational.schedule', inverse_name='church_id',
                                                string='Jadwal Ibadah')
    @api.depends(
        'street',
        'zip',
        'city',
        'city_id',
        'country_id',
        'state_id',
    )
    def _compute_address(self):
        for rec in self:
            state = rec.state_id.name if rec.state_id else ''
            country = rec.country_id.name if rec.country_id else ''
            rec.full_address = f"""
                    {rec.street}, {rec.city}, {state}, {country} {rec.zip}
                """

    parent_id = fields.Many2one(comodel_name='gereja', string='Cabang/Ranting Dari', ondelete='set null')
    jemaat_line = fields.One2many(comodel_name='jemaat', inverse_name='gereja_id', string='Jemaat')
    cool_line_id = fields.One2many(comodel_name='cool', inverse_name='gereja_id', string='Cool')

    image_1920 = fields.Image("Foto Gereja", max_width=1920, max_height=1920)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
    ], 'Status', default="draft")
    active = fields.Boolean(string='Aktif', default=True)
    _sql_constraints = [
        ('nomor_uniq', 'unique(sequence)', "nomor already exists !"),
        ('name_uniq', 'unique(name)', "nama already exists !"),
    ]

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
            self.zip = self.city_id.zipcode
            self.state_id = self.city_id.state_id
        elif self._origin:
            self.city = False
            self.zip = False
            self.state_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['create_date'])
                ) if 'create_date' in vals else None
                vals['sequence'] = (self.env.ref('custom_addons.app_gereja_sequence').
                                    next_by_code('app.gereja.seq', sequence_date=seq_date) or _("New"))

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
