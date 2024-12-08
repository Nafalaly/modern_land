#  -*- coding: utf-8 -*-
from odoo import models, fields, api


class Gereja(models.Model):
    _name = 'gereja'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'data Gereja'
    _rec_name = 'name'

    _rec_seq_fields_name = {
        'sequence': 'app.gereja.seq'
    }

    sequence = fields.Char('Nomor Gereja', index=True, readonly=True, help='No Urut')
    name = fields.Char('Nama Gereja', required=True)
    gembala_id = fields.Many2one(comodel_name='pengerja', string='Nama Gembala', ondelete='restrict')
    rank_id = fields.Many2one(comodel_name='rank', string='Rank Gereja', ondelete='restrict')

    # as default Chruch will always in confirm state,
    # in case need two ways validation then remove this code
    state = fields.Selection(default="confirm")

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
    full_address = fields.Char(string='Alamat', help='Help to search full address', compute='_compute_address',
                               store=True)

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
    jemaat_line = fields.One2many(comodel_name='res.partner', inverse_name='gereja_id', string='Jemaat')
    cool_line_id = fields.One2many(comodel_name='cool', inverse_name='gereja_id', string='Cool')

    image_1920 = fields.Image("Foto Gereja", max_width=1920, max_height=1920)
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
