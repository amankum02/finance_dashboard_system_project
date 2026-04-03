from odoo import models, api
from datetime import date, timedelta
from collections import defaultdict


class FinanceDashboard(models.AbstractModel):
    _name = 'finance.dashboard'
    _description = 'Finance Dashboard'

    @api.model
    def get_summary(self):
        FinanceRecord = self.env['finance.record']
        total_income = sum(
            FinanceRecord.search([('type', '=', 'income')]).mapped('amount')
        )
        total_expense = sum(
            FinanceRecord.search([('type', '=', 'expense')]).mapped('amount')
        )
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': total_income - total_expense,
        }

    @api.model
    def get_category_totals(self):
        records = self.env['finance.record'].search([])
        totals = defaultdict(lambda: {'income': 0.0, 'expense': 0.0})
        for r in records:
            category = r.category or 'Uncategorized'
            totals[category][r.type] += r.amount
        return [
            {
                'category': cat,
                'income': vals['income'],
                'expense': vals['expense'],
                'net': vals['income'] - vals['expense'],
            }
            for cat, vals in totals.items()
        ]

    @api.model
    def get_recent_activity(self, limit=10):
        records = self.env['finance.record'].search(
            [], limit=limit, order='date desc'
        )
        return [
            {
                'id': r.id,
                'date': str(r.date),
                'type': r.type,
                'category': r.category or 'Uncategorized',
                'amount': r.amount,
                'currency': r.currency_id.symbol,
                'notes': r.notes or '',
            }
            for r in records
        ]

    @api.model
    def get_monthly_trends(self):
        current_year = date.today().year
        records = self.env['finance.record'].search([
            ('date', '>=', date(current_year, 1, 1)),
            ('date', '<=', date(current_year, 12, 31)),
        ])
        monthly = defaultdict(lambda: {'income': 0.0, 'expense': 0.0})
        for r in records:
            key = r.date.strftime('%Y-%m')
            monthly[key][r.type] += r.amount
        return [
            {
                'month': month,
                'income': vals['income'],
                'expense': vals['expense'],
                'net': vals['income'] - vals['expense'],
            }
            for month, vals in sorted(monthly.items())
        ]

    @api.model
    def get_weekly_trends(self):
        today = date.today()
        eight_weeks_ago = today - timedelta(weeks=8)
        records = self.env['finance.record'].search([
            ('date', '>=', eight_weeks_ago)
        ])
        weekly = defaultdict(lambda: {'income': 0.0, 'expense': 0.0})
        for r in records:
            key = r.date.strftime('%Y-W%W')
            weekly[key][r.type] += r.amount
        return [
            {
                'week': week,
                'income': vals['income'],
                'expense': vals['expense'],
                'net': vals['income'] - vals['expense'],
            }
            for week, vals in sorted(weekly.items())
        ]

    @api.model
    def get_dashboard_data(self):
        return {
            'summary': self.get_summary(),
            'category_totals': self.get_category_totals(),
            'recent_activity': self.get_recent_activity(limit=10),
            'monthly_trends': self.get_monthly_trends(),
            'weekly_trends': self.get_weekly_trends(),
        }