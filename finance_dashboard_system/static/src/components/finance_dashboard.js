/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
import { Component, onMounted, onPatched, useState, useRef } from '@odoo/owl';

export class FinanceDashboard extends Component {
    static template = 'finance.Dashboard';

    setup() {
        this.orm = useService('orm');
        this.action=useService('action');
        this.chartRef = useRef('financeChart');
        this.chartRendered = false;
        this.state = useState({
            summary: {},
            categoryTotals: [],
            recentActivity: [],
            monthlyTrends: [],
            loading: true,
        });
        onMounted(() => this.loadDashboard());
        onPatched(() => {
            if (!this.state.loading && !this.chartRendered) {
                this.renderChart();
            }
        });
        
    }

    async loadDashboard() {
        const [summary, categoryTotals, recentActivity, monthlyTrends] = await Promise.all([
            this.orm.call('finance.dashboard', 'get_summary', []),
            this.orm.call('finance.dashboard', 'get_category_totals', []),
            this.orm.call('finance.dashboard', 'get_recent_activity', []),
            this.orm.call('finance.dashboard', 'get_monthly_trends', []),
        ]);

        this.state.summary = summary;
        this.state.categoryTotals = categoryTotals;
        this.state.recentActivity = recentActivity;
        this.state.monthlyTrends = monthlyTrends;
        this.state.loading = false;
    }

    openIncomeList() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Income Records',
            res_model: 'finance.record',
            view_mode: 'list,form',
            views: [[false, 'list'], [false, 'form']],
            domain: [['type', '=', 'income']],
            context: { default_type: 'income' },
        });
    }

    openExpenseList() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Expense Records',
            res_model: 'finance.record',
            view_mode: 'list,form',
            views: [[false, 'list'], [false, 'form']],
            domain: [['type', '=', 'expense']],
            context: { default_type: 'expense' },
        });
    }

    openAllList() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'All Records',
            res_model: 'finance.record',
            view_mode: 'list,form',
            views: [[false, 'list'], [false, 'form']],
            domain: [],
        });
    }

    openRecord(id) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Finance Record',
            res_model: 'finance.record',
            view_mode: 'form',
            views: [[false, 'form']],
            res_id: id,
        });
    }

    renderChart() {
        const canvas = this.chartRef.el;

        if (!canvas) {
            console.error('Canvas not found!');
            return;
        }

        if (!this.state.monthlyTrends.length) {
            console.warn('No monthly trends data!');
            return;
        }

        this.chartRendered = true;

        const labels = this.state.monthlyTrends.map(m => m.month);
        const incomeData = this.state.monthlyTrends.map(m => m.income);
        const expenseData = this.state.monthlyTrends.map(m => m.expense);

        new Chart(canvas, {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Income',
                        data: incomeData,
                        backgroundColor: '#1D9E75',
                        borderRadius: 6,
                    },
                    {
                        label: 'Expense',
                        data: expenseData,
                        backgroundColor: '#E24B4A',
                        borderRadius: 6,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'top' } },
                scales: {
                    y: { beginAtZero: true },
                    x: { grid: { display: false } },
                },
            },
        });
    }
}

registry.category('actions').add('finance.dashboard', FinanceDashboard);