from odoo import models, fields


class Rank(models.Model):
    _name = 'rank'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'data rank gereja'
    _rec_name = 'name'

    name = fields.Char(strng='Rank Gereja', required=True)
    # TODO: Additional Info (?)
    main = fields.Boolean(string='Pusat')
    sequence = fields.Integer(string='Sequence')

    rank_line_ids = fields.One2many(comodel_name='gereja', inverse_name='rank_id', string='Rank Gereja')
