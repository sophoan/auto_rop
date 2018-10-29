# -*- coding: utf-8 -*-
from odoo import http

# class AutoRop(http.Controller):
#     @http.route('/auto_rop/auto_rop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/auto_rop/auto_rop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('auto_rop.listing', {
#             'root': '/auto_rop/auto_rop',
#             'objects': http.request.env['auto_rop.auto_rop'].search([]),
#         })

#     @http.route('/auto_rop/auto_rop/objects/<model("auto_rop.auto_rop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('auto_rop.object', {
#             'object': obj
#         })