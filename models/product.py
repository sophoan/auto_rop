# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

class ProductTemplate(models.Model):
    _inherit = "product.template"

    enable_auto_rop = fields.Boolean('Enable Auto ROP', default=True, help="If unchecked, the auto rop feature for this product will not triggered.")


class Product(models.Model):
    _inherit = "product.product"

    order_line_ids = fields.One2many('purchase.order.line', 'product_id')

    @api.model
    def compute_rop(self, use_new_cursor=False):
        self.ensure_one()
        if self.categ_id is not None and self.categ_id.enable_auto_rop == False:
            return
        if self.enable_auto_rop == False:
            return
        processor = ROPProcessor()
        processor.calculate_rop(self, use_new_cursor=True)


class ProductCategory(models.Model):
    _inherit = "product.category"

    enable_auto_rop = fields.Boolean('Enable Auto ROP', default=True,
                                     help="If unchecked, the auto rop feature for this product will not triggered.")


class ROPProcessor():


    def calculate_rop(self, product, use_new_cursor=False):

        rop_forecaster = ROPForecaster()

        for orderpoint in product.orderpoint_ids:
            rop_data = rop_forecaster.get_forecasted_rop(product)
            if rop_data == None:
                return

            self.save_rop_result(product.env['auto_rop.rop'],rop_data)
            if use_new_cursor:
                product._cr.commit()

            self.update_reorder_rule(orderpoint, {
                'product_min_qty': rop_data['min_qty'],
                'product_max_qty': rop_data['max_qty'],
                'lead_days': rop_data['lead_time_in_days']
            })
            if use_new_cursor:
                product._cr.commit()



    def save_rop_result(self, rop, rop_data):
        # print("Save ROP: {0}".format(rop_data))
        r = rop.create(rop_data)
        # print(r.product_id.name)

    def update_reorder_rule(self, orderpoint, updated_data):
        # print("Update Rule: {0}".format(updated_data))
        orderpoint.write(updated_data)


class ROPForecaster():


    def __init__(self):
        self._lead_time_forecaster = MovingAverageLeadTimeForecaster()
        self._sale_forecaster = MovingAverageSaleForecaster()

    def get_forecasted_rop(self, product):
        # print("Product: {0}".format(product.name))

        lead_time = self._lead_time_forecaster.get(product)

        # print("Lead time: {0}".format(lead_time))

        sale = self._sale_forecaster.get_for_next_ndays(product, lead_time)
        # print("Sale: {0}".format(sale))


        for orderpoint in product.orderpoint_ids:
            last_min_qty = orderpoint.product_min_qty
            last_max_qty = orderpoint.product_max_qty
            last_lead_time = orderpoint.lead_days
            safety_qty = orderpoint.product_safety_qty

            new_lead_time = lead_time if lead_time > 0 else last_lead_time
            new_min_qty = safety_qty + sale
            new_max_qty = new_min_qty + sale

            return {
                'product_id': product.id,
                'product_safety_qty': safety_qty,
                'lead_time_in_days': new_lead_time,
                'forecasted_sale': sale,
                'min_qty': new_min_qty,
                'max_qty': new_max_qty
            }


class SaleForecaster():
    def get_for_next_ndays(self, product, days):
        pass


class LeadTimeForecaster():
    def get(self, product):
        pass


class MovingAverageLeadTimeForecaster():
    def get(self, product):
        #product.order_line_ids.filtered(lambda o: o.order_id.state == 'purchase').ids
        orders = product.env['purchase.order'].search([('order_line.product_id', '=', product.id),
                                                       ('state', '=', 'purchase')], limit=10, order='date_order desc')
        lead_time_days = 0
        n = 0
        for order in orders:
            for picking in order.picking_ids.search([('state', '=', 'done')]):
                lead_time_days += (fields.Datetime.from_string(picking.date_done) - fields.Datetime.from_string(order.date_order)).days
                n += 1
        if n == 0:
            return 0
        return  round(lead_time_days / n)


class MovingAverageSaleForecaster(SaleForecaster):
    def get_for_next_ndays(self, product, days):
        if days == 0:
            return 0
        date_1 = fields.Datetime.to_string((fields.Datetime.from_string(fields.Datetime.now()) - timedelta(days=days*6)))
        date_2 = fields.Datetime.to_string((fields.Datetime.from_string(fields.Datetime.now()) - timedelta(days=365)))
        date_3 = fields.Datetime.to_string((fields.Datetime.from_string(fields.Datetime.now()) - timedelta(days=365-days*3)))
        sales = product.env['sale.order'].search([('order_line.product_id', '=', product.id),
                                                     ('state', '=', 'sale'),
                                                     '|', ('date_order', '>=', date_1),
                                                     '&', ('date_order', '<=', date_2),
                                                    ('date_order', '>=', date_3)],
                                                     order='date_order desc')
        total_sale = 0
        n = 0
        for sale in sales:
            for line in sale.order_line.search([('product_id', '=', product.id)]):
                total_sale += line.product_uom_qty
                n += 1
        print("Forecast sale: {0}, {1}".format(total_sale, n))
        if total_sale == 0:
            return 0
        return total_sale / 9