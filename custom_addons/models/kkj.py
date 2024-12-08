from odoo import models, fields
from odoo.tools.translate import _


class KartuKeluargaJemaat(models.Model):
    _name = 'kartu.keluarga.jemaat'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'gbi.base.document']
    _description = 'Kartu keluarga jemaat'
    _rec_name = 'nomor'

    _rec_seq_fields_name = {
        'nomor': 'app.kkj.seq'
    }

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

    _sql_constraints = [
        ('nomor_uniq', 'unique (nomor)', "nomor already exists !"),
    ]

    pengerja_line_ids = fields.One2many(comodel_name='pengerja', inverse_name='nomor_kkj', string='Pengerja')

    # TODO: Confirm Button in XML
