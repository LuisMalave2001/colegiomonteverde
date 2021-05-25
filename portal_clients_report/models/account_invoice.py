# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.depends('date_invoice')
    def _compute_invoice_month(self):
        for rec in self:
            if rec.date_invoice:
                rec.invoice_month = rec.date_invoice.strftime("%B")
            else:
                rec.invoice_month = ""

    def _compute_xml_attach_id(self):
        IrAttachment = self.env['ir.attachment']
        for rec in self:
            attch_id = IrAttachment.search([
                ('res_id', '=', rec.id),
                ('res_model', '=', 'account.invoice'),
                ('type', '=', 'binary'),
                ('mimetype', '=', 'application/xml')
            ], limit=1)
            rec.xml_attach_id = attch_id if attch_id else False

    invoice_month = fields.Char(string="Invoices of the Months of:", compute="_compute_invoice_month")
    concept = fields.Char(string="Concept")
    xml_attach_id = fields.Many2one('ir.attachment', compute="_compute_xml_attach_id", string="Attachment")
