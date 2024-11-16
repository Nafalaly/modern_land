# -*- coding: utf-8 -*-
from odoo import api, fields, models, api
from odoo.exceptions import ValidationError


class MasterApproval(models.Model):
    _name = "master.approval"
    _description = 'Master Approval'

    name = fields.Char('Name')
    model_name = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade')
    notification_mail_template = fields.Many2one('mail.template', string="Notification Template", required=True, domain="[('model_id', '=', model_name)]")
    notification_approved_mail_template = fields.Many2one('mail.template', string="Notification Approved Template",
                                                          required=True, domain="[('model_id', '=', model_name)]")
    notification_rejected_mail_template = fields.Many2one('mail.template', string="Notification Rejected Template",
                                                          required=True, domain="[('model_id', '=', model_name)]")
    line_ids = fields.One2many('master.approval.line', 'config_id', string="Approval Lines", required=True)
    current_active = fields.Boolean(string="Active", default=True)
    mail_activity_type_id = fields.Many2one('mail.activity.type', 'Notification Activity Type',
                                            required=True)
    lead_time = fields.Integer(string="Lead time in Days", default=1)

    @api.constrains('line_ids')
    def ensure_approval_is_filled(self):
        if not self.line_ids:
            raise ValidationError('Approval harus di isi !')


class MasterApprovalLine(models.Model):
    _name = "master.approval.line"
    _description = "Master Approval Line"

    config_id = fields.Many2one('master.approval', string='Config ID', required=True)
    users_id = fields.Many2one('res.users', string='User Approver', domain=[("groups_id", "ilike", "Internal User")], required=True)
    sequence = fields.Integer(string='Sequence')

    @api.constrains('users_id')
    def _email_required(self):
        for line in self:
            if not line.users_id.partner_id.email:
                raise ValidationError('Please Configure Email for %s' % line.users_id.partner_id.name)


class ListApproval(models.Model):
    _name = "list.approval"
    _description = "List Approval"

    users_id = fields.Many2one('res.users', string='User Approver', domain=[("groups_id", "ilike", "Internal User")], required=True)
    sequence = fields.Integer(string='Sequence')
    assigned_date = fields.Datetime(string="Assigned Date", default=fields.Date.today())
    state = fields.Selection([
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('reject', 'Rejected'),
        ('invalid', 'Invalid'),
    ], default='pending')
    validation_date = fields.Date(string='Validation Date')
    note = fields.Text(string='Reason')

    related_model_id = fields.Many2one('ir.model', string='Related Model')
    related_record_id = fields.Integer(string='Related Record ID')
    related_record = fields.Reference(selection='_get_available_record', string='Related Record')

    @api.model
    def _get_available_records(self):
        if self.related_model_id:
            related_model = self.env['ir.model'].browse(self.related_model_id)
            model_obj = self.env[related_model.model]
            return [(record.id, record.display_name) for record in model_obj.search([])]
        else:
            return []