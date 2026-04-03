from odoo import models, fields,api
from odoo.exceptions import ValidationError, UserError
from datetime import date

class FinanceRecord(models.Model):
    _name = 'finance.record'
    _description = 'Financial Records'
    _order = 'date desc'

    amount = fields.Monetary(string="Amount", required=True)
    
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    type = fields.Selection([
        ('income', 'Income'),
        ('expense', 'Expense')
    ], string="Type", required=True)

    category = fields.Char(string="Category")
    
    date = fields.Date(string="Date", required=True, default=fields.Date.today)

    notes = fields.Text(string="Notes")
    
    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError(
                    "Amount must be greater than zero. "
                    f"Received: {record.amount}"
                )

    @api.constrains('date')
    def _check_date(self):
        for record in self:
            if record.date > date.today():
                raise ValidationError(
                    f"Date cannot be in the future. "
                    f"Received: {record.date}"
                )

    @api.constrains('category')
    def _check_category(self):
        for record in self:
            if record.category and len(record.category.strip()) < 2:
                raise ValidationError(
                    "Category must be at least 2 characters long."
                )
            if record.category and len(record.category) > 100:
                raise ValidationError(
                    "Category cannot exceed 100 characters."
                )

    @api.onchange('amount')
    def _onchange_amount_warning(self):
        if self.amount and self.amount > 1_000_000:
            return {
                'warning': {
                    'title': 'Large Amount',
                    'message': f'Amount {self.amount:,.2f} is unusually large. Please verify.'
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Strip whitespace from category
            if vals.get('category'):
                vals['category'] = vals['category'].strip()

            # Ensure notes don't exceed limit
            if vals.get('notes') and len(vals['notes']) > 1000:
                raise ValidationError(
                    "Notes cannot exceed 1000 characters."
                )

        return super().create(vals_list)

    def write(self, vals):
        # Prevent amount change if record is too old (>1 year)
        if 'amount' in vals:
            for record in self:
                days_old = (date.today() - record.date).days
                if days_old > 365:
                    raise UserError(
                        f"Record '{record.id}' is over a year old. "
                        "Amount cannot be modified for old records."
                    )

        if vals.get('category'):
            vals['category'] = vals['category'].strip()

        if vals.get('notes') and len(vals['notes']) > 1000:
            raise ValidationError(
                "Notes cannot exceed 1000 characters."
            )

        return super().write(vals)
