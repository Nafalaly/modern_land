#  -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class BaseDocument(models.AbstractModel):
    """
    GBI Base Document Mixin

    This abstract model is designed to provide a reusable base for handling
    document workflows in Odoo. It helps reduce code duplication and promotes
    code reuse across multiple models that follow a similar workflow pattern.
    """
    _name = 'gbi.base.document'
    _description = 'GBI Base Document mixin'

    # USAGES: {'nomor': 'app.baptisan.seq'}
    _rec_seq_fields_name = {}

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], 'Status', default="draft")

    @api.model_create_multi
    def create(self, vals_list):
        """
        Handles the sequence in documents after creation
        """
        for vals in vals_list:
            for field in self._rec_seq_fields_name.keys():

                seq_code = self._rec_seq_fields_name[field]

                if vals.get(field, _("New")) == _("New"):
                    seq_date = fields.Datetime.context_timestamp(
                        self, fields.Datetime.to_datetime(vals['create_date'])
                    ) if 'create_date' in vals else None
                    vals[field] = self.env['ir.sequence'].next_by_code(
                        seq_code, sequence_date=seq_date) or _("New")

        return super().create(vals_list)

    def _action_confirm(self):
        _logger.info(f"""Document {self._name}:{self.id} is Confirmed""")
        self.state = 'confirm'

    def action_confirm(self):
        self._action_confirm()

    def _action_reset_to_draft(self):
        _logger.info(f"""Document {self._name}:{self.id} is set to Draft""")
        self.state = 'draft'

    def action_reset_to_draft(self):
        self._action_reset_to_draft()

    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise ValidationError(f"""Tidak bisa menghapus {self._description} yang sudah dikonfirmasi""")
        res = super(BaseDocument, self).unlink()
        return res
