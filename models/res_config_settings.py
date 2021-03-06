# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class auto_rop(models.Model):
#     _name = 'auto_rop.auto_rop'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_feature = fields.Boolean("Enable/Disable")
