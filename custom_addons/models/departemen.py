from odoo import models, fields

class Rank(models.Model):
    _name = 'departemen'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data departemen'
    _rec_name = 'name'

    name = fields.Char(strng='Departemen', required=True)
    kode = fields.Char(string='Kode Departemen')
    sequence = fields.Integer(string='Sequence')