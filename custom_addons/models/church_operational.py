#  -*- coding: utf-8 -*-
from odoo import models, fields


class ChruchOperational(models.Model):
    _name = 'chruch.operational.schedule'
    _description = 'Chruch Operational Schedule'
    _rec_name = 'display_name'
    _order = 'start_time'

    display_name = fields.Char()
    church_id = fields.Many2one(comodel_name='gereja', string='Gereja', ondelete='cascade')
    church_activity_type_id = fields.Many2one(comodel_name='church.activity.type', string='Ibadah',
                                              required=True, ondelete='restrict', help='Activity type of Schedule')
    start_time = fields.Char(string='Jam', required=True, help='Start Time')





