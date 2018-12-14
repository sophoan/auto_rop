# -*- coding: utf-8 -*-

from odoo import models, fields, api, registry, _
from odoo.addons import decimal_precision as dp

import logging
import threading

class OrderPoint(models.Model):
    _name = "stock.warehouse.orderpoint"
    _inherit = ["stock.warehouse.orderpoint", "mail.thread"]

    lead_days = fields.Integer(
        'Lead Time', default=1,
        help="Number of days after the orderpoint is triggered to receive the products or to order to the vendor",
        track_visibility='onchange'
    )

    product_safety_qty = fields.Float(
        "Safety Quantity", digits=dp.get_precision("Product Unit of Measure"), default=0, required=True,
        help="The reserved stock to cover in case of delaying in receiving products."
    )

    @api.model
    def run_scheduler(self, use_new_cursor=False):
        # print("Run Scheduler")
        try:
            if use_new_cursor:
                cr = registry(self._cr.dbname).cursor()
                self = self.with_env(self.env(cr=cr))
            for orderpoint in self.sudo().search([]):
                orderpoint.product_id.compute_rop(use_new_cursor=True)
            self._cr.commit()
        finally:
            if use_new_cursor:
                try:
                    self._cr.close()
                except Exception:
                    pass
        return {}


































