from odoo import http
from odoo.http import request


class WebsiteCustomers(http.Controller):
    @http.route(["/customers"], type="http", auth="public", website=True)
    def customers_page(self, **kwargs):
        customers = request.env["res.partner"].sudo().search([])
        return request.render(
            "crm_socials.customers_template", {"customers": customers}
        )

    @http.route("/search", type="http", auth="public", website=True)
    def search_customers(self, **kw):
        search_query = kw.get("q", "")

        domain = [
            "|",
            ("name", "ilike", search_query),
            "|",
            ("facebook_url", "ilike", search_query),
            "|",
            ("linkedin_url", "ilike", search_query),
            ("x_url", "ilike", search_query),
        ]

        customers = request.env["res.partner"].search(domain)

        return request.render(
            "crm_socials.customers_template",
            {"customers": customers, "query": search_query},
        )
