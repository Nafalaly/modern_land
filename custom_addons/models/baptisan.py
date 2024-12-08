from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Baptisan(models.Model):
    _name = 'baptisan'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'data Baptisan'
    _rec_name = 'nama_jemaat_id'

    _rec_seq_fields_name = {
        'nomor': 'app.baptisan.seq'
    }

    nomor = fields.Char('Nomor Baptisan', required=True, index=True, readonly=True, default=lambda self: _('New'))
    nama_jemaat_id = fields.Many2one(comodel_name='res.partner', string='Nama Jemaat', required=True, index=True)
    nama_pendeta_id = fields.Many2one(comodel_name='pengerja', string='Pendeta yang membaptis',
                                      domain="[('id','in',allowed_pendeta_ids)]")

    allowed_pendeta_ids = fields.Many2many(comodel_name='pengerja', compute='_compute_allowed_pendeta_ids')

    @api.depends('nama_pendeta_id')
    def _compute_allowed_pendeta_ids(self):
        self.ensure_one()
        sql = """
            SELECT DISTINCT
                ppl.pengerja_id as pengerja_id
            FROM 
                pengerja_pelayanan_line as ppl
            LEFT JOIN bidang_pelayanan bp on (bp.id=ppl.pelayanan_id)
            WHERE bp.pelayanan_gembala = True
        """
        self._cr.execute(sql)
        raw_results = self._cr.dictfetchall()
        self.allowed_pendeta_ids = [item['pengerja_id'] for item in raw_results]

    tempat_baptis = fields.Char(string='Tempat Baptis')
    tanggal_baptis = fields.Date(string='Tanggal Baptis')
    gereja_id = fields.Many2one(comodel_name='gereja', string='Nama Gereja', ondelete='set null')
    image_1920 = fields.Image("Foto Baptisan", max_width=1920, max_height=1920)
    jemaat_ids = fields.Many2many(comodel_name='res.partner', string='Jemaat', domain=[('is_jemaat', '=', True)])

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

    pengerja_line = fields.Many2many(comodel_name='pengerja', string='Pengerja')

    def _ensure_baptis(self):
        jemaat_id = self.search([
            ('nama_jemaat_id', '=', self.nama_jemaat_id.id),
            ('state', '=', 'confirm'),
        ], limit=1)
        if jemaat_id:
            raise ValidationError('Jemaat sudah di baptis')

    def action_confirm(self):
        self._ensure_baptis()
        super(Baptisan, self).action_confirm()
