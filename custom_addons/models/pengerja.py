from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Pengerja(models.Model):
    _name = 'pengerja'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'data Pengerja/Gembala'
    _rec_name = 'display_name'

    _rec_seq_fields_name = {
        'nomor': 'app.pengerja.seq'
    }

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

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

    baptisan_line_ids = fields.One2many(comodel_name='baptisan', inverse_name='nama_pendeta_id',
                                        string='Pendeta yang membaptis')
    gereja_line_ids = fields.One2many(comodel_name='gereja', inverse_name='gembala_id', string='Nama Gembala')

    def _ensure_only_one(self):
        pengerja_id = self.search([
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'confirm'),
        ], limit=1)
        if pengerja_id:
            raise ValidationError('Pengerja sudah di buat')

    def action_confirm(self):
        self._ensure_only_one()
        super(Pengerja, self).action_confirm()
