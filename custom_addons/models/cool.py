from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)


class Cool(models.Model):
    _name = 'cool'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data cool'
    _rec_name = 'name'

    name = fields.Char('Nama Cool', required=True)
    gereja_id = fields.Many2one(comodel_name='gereja', string='Cabang/Ranting', required=True)
    name_cooler = fields.Many2one(comodel_name='res.partner', string='Nama COOLer', domain=[('is_jemaat', '=', True)], required=True)
    jenis_cooler = fields.Selection([
        ('anak', 'Anak'),
        ('dm', 'DM'),
        ('doa', 'Doa'),
        ('jc', 'JC'),
        ('musik', 'Musik'),
        ('umas', 'Umas'),
        ('umum', 'Umum'),
        ('wanita', 'Wanita'),
        ('youth', 'Youth'),
    ], string='Jenis COOLer')
    tanggal_cool = fields.Date(string='Tanggal')
    tempat = fields.Char(string='Tempat')
    waktu_start = fields.Char(string='Waktu Mulai')
    waktu_end = fields.Char(string='Sampai')
    tema = fields.Char(string='Tema')
    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    persembahan = fields.Monetary(string="Persembahan")
    state = fields.Selection([
        ('active', 'Active'),
        ('not active', 'Not Active'),
    ], 'Status', default="active")

    cool_anggota_line = fields.One2many(comodel_name='cool.anggota', inverse_name='cool_id')
    cool_kubu_doa_line = fields.One2many(comodel_name='cool.kubu.doa', inverse_name='cool_id')

    def action_cancel(self):
        self.change_state('not active')

    def _compute_time(self):
        return True


class CoolAnggota(models.Model):
    _name = 'cool.anggota'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data anggota cool'
    _rec_name = 'cool_id'

    cool_id = fields.Many2one(comodel_name='cool', string='Cool ID')
    jemaat_id = fields.Many2one(comodel_name='res.partner', string='Anggota', domain=[('is_jemaat', '=', True)])
    tanggal_gabung = fields.Date(string='Tanggal Gabung')
    anggota_baru = fields.Boolean(string='Anggota Baru ?', default=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='active')


class CoolKubuDoa(models.Model):
    _name = 'cool.kubu.doa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data anggota cool kubu doa'
    _rec_name = 'cool_id'

    cool_id = fields.Many2one(comodel_name='cool', string='Cool ID')
    jemaat_id = fields.Many2one(comodel_name='res.partner', string='Anggota', domain=[('is_jemaat', '=', True)])
    tanggal_gabung = fields.Date(string='Tanggal Gabung')
    anggota_baru = fields.Boolean(string='Anggota Baru ?', compute='_set_anggota')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='active')

    def _set_anggota(self):
        for line in self:
            if line.create_date:
                line.anggota_baru = True if datetime.strptime(line.create_date, "%Y-%m-%d") > datetime.now() else False
