# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string="cancel day" , config_parameter='om_hospital.cancel_days')
