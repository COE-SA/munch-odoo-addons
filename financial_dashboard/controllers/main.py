from odoo import http
from odoo.http import request


class FinancialDashboard(http.Controller):

    @http.route('/financial-dashboard', type='http', auth='user', website=False)
    def dashboard(self, **kwargs):
        return request.render('financial_dashboard.main_template', {
            'user_name': request.env.user.name,
        })
