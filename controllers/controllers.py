# -*- coding: utf-8 -*-
# from odoo import http


# class JtGs1Gtin(http.Controller):
#     @http.route('/jt_gs1_gtin/jt_gs1_gtin', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jt_gs1_gtin/jt_gs1_gtin/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jt_gs1_gtin.listing', {
#             'root': '/jt_gs1_gtin/jt_gs1_gtin',
#             'objects': http.request.env['jt_gs1_gtin.jt_gs1_gtin'].search([]),
#         })

#     @http.route('/jt_gs1_gtin/jt_gs1_gtin/objects/<model("jt_gs1_gtin.jt_gs1_gtin"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jt_gs1_gtin.object', {
#             'object': obj
#         })
