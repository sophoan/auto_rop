# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

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

class ROP(models.Model):
    _name = "auto_rop.rop"

    calculated_date = fields.Datetime(default=fields.datetime.now())
    product_safety_qty = fields.Float(
        "Safety Quantity", digits=dp.get_precision("Product Unit of Measure"), default=0, required=True,
        help="The reserved stock to cover in case of delaying in receiving products."
    )
    lead_time_in_days = fields.Float()
    forecasted_sale = fields.Float(digits=(6,2), string="Forecasted Sale Amount")
    min_qty = fields.Float(string="Min Qty to Order")
    max_qty = fields.Float(string="Max Qty to Order")

    product_id = fields.Many2one('product.product', string="Product")