from odoo import http
from odoo.http import request


class WebsiteCustomers(http.Controller):
    @http.route(["/customers"], type="http", auth="public", website=True)
    def customers_page(self, **kwargs):
        customers = request.env["res.partner"].sudo().search([])
        return request.render(
            "crm_socials.customers_template", {"customers": customers}
        )
