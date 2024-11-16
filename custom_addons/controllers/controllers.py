# -*- coding: utf-8 -*-
# from odoo import http


# class CustomAjun(http.Controller):
#     @http.route('/custom_addons/custom_addons', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_addons/custom_addons/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_addons.listing', {
#             'root': '/custom_addons/custom_addons',
#             'objects': http.request.env['custom_addons.custom_addons'].search([]),
#         })

#     @http.route('/custom_addons/custom_addons/objects/<model("custom_addons.custom_addons"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_addons.object', {
#             'object': obj
#         })
