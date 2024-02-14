from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    company_phone = fields.Char(string='company Phone')


    def test(self):
        print("m000000000")
