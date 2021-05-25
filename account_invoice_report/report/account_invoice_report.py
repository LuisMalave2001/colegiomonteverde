# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import tools
from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    discount_amount = fields.Float(string='Discount Amount', readonly=True)
    origin = fields.Char(string='Source Document', readonly=True)

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total_company_signed', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
            'journal_id', 'number', 'partner_bank_id', 'partner_id', 'payment_term_id',
            'residual', 'state', 'type', 'user_id', 'discount_amount', 'origin'
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uom_id', 'account_analytic_id', 'discount'
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.discount_amount as discount_amount, sub.origin"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ", ai.discount_amount as discount_amount, ai.origin"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", ai.discount_amount, ai.origin"
