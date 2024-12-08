from odoo import models, fields


class Department(models.Model):
    """
    Inherit from Operating.unit
    """
    _inherit = ['operating.unit']
    _description = 'Data Department'
    _rec_name = 'name'

    name = fields.Char(strng='Departemen')
    code = fields.Char(string='Kode Departemen')

    def _get_default_partner_id(self):
        """
        Set default partner_id to Company
        """
        partner_id = self.env.ref('base.main_partner')
        return partner_id

    partner_id = fields.Many2one(default=_get_default_partner_id)
