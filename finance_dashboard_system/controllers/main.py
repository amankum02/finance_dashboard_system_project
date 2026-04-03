from odoo import http
from odoo.http import request, Response
from odoo.exceptions import AccessError
import json


class FinanceDashboardController(http.Controller):

    def _check_access(self, group_xml_id):
        if not request.env.user.has_group(group_xml_id):
            raise AccessError("You do not have permission to access this resource.")

    @http.route('/api/finance/dashboard', type='http', auth='user', methods=['GET'], csrf=False)
    def get_dashboard(self):
        try:
            self._check_access('finance_dashboard_system.group_viewer')
            data = request.env['finance.dashboard'].get_dashboard_data()
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except AccessError as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                status=403,
                content_type='application/json'
            )

    @http.route('/api/finance/summary', type='http', auth='user', methods=['GET'], csrf=False)
    def get_summary(self):
        try:
            self._check_access('finance_dashboard_system.group_analyst')
            data = request.env['finance.dashboard'].get_summary()
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except AccessError as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                status=403,
                content_type='application/json'
            )

    @http.route('/api/finance/category-totals', type='http', auth='user', methods=['GET'], csrf=False)
    def get_category_totals(self):
        try:
            self._check_access('finance_dashboard_system.group_analyst')
            data = request.env['finance.dashboard'].get_category_totals()
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except AccessError as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                status=403,
                content_type='application/json'
            )

    @http.route('/api/finance/recent-activity', type='http', auth='user', methods=['GET'], csrf=False)
    def get_recent_activity(self):
        try:
            self._check_access('finance_dashboard_system.group_viewer')
            limit = int(request.params.get('limit', 10))
            data = request.env['finance.dashboard'].get_recent_activity(limit=limit)
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except AccessError as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                status=403,
                content_type='application/json'
            )

    @http.route('/api/finance/monthly-trends', type='http', auth='user', methods=['GET'], csrf=False)
    def get_monthly_trends(self):
        try:
            self._check_access('finance_dashboard_system.group_analyst')
            data = request.env['finance.dashboard'].get_monthly_trends()
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except AccessError as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                status=403,
                content_type='application/json'
            )

    @http.route('/api/finance/weekly-trends', type='http', auth='user', methods=['GET'], csrf=False)
    def get_weekly_trends(self):
        try:
            self._check_access('finance_dashboard_system.group_analyst')
            data = request.env['finance.dashboard'].get_weekly_trends()
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except AccessError as e:
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                status=403,
                content_type='application/json'
            )