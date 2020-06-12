import base64
from datetime import datetime
from io import BytesIO
import calendar

from odoo import api, fields, models, _
from odoo.tools.misc import xlwt


class StockConsignmentReport(models.TransientModel):
    _name = 'stock.consignment.report'

    from_date = fields.Date(string='Date From')
    to_date = fields.Date(string='Date To')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')
    excel_file = fields.Binary('Excel File')
    file_name = fields.Char('Excel File', size=64)
    inventory_printed = fields.Boolean(string='Payment Report Printed')

    @api.multi
    def consignment_stock_report_print(self):
        self.file_name = 'filename.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')
        # style = xlwt.easyxf('font: bold True, name Arial;')
        worksheet.write_merge(0, 1, 0, 3, 'your data that you want to show into excelsheet')
        fp = BytesIO()
        workbook.save(fp)
        self.file_name = 'Long roll Report.xls'
        record_id = self.env['stock.consignment.report'].create({'excel_file': base64.encodestring(fp.getvalue()),
                                                                'file_name': self.file_name}, )
        fp.close()
        return {
            'view_mode': 'form',
            'res_id': record_id.id,
            'res_model': 'stock.consignment.report',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
            'target': 'new',
        }
