
from odoo import fields,models,api
class SaleOrder(models.Model):
    
    _inherit="sale.order"
    
    cancel_date=fields.Datetime(string="Cancel Date",readonly=True)
        
    @api.multi
    def action_cancel(self):
        super(SaleOrder, self).action_cancel()
        self.write({
            'cancel_date':fields.Datetime.now()
            
    })
    
    @api.multi
    def action_draft(self):
        super(SaleOrder, self).action_draft()
        self.write({'cancel_date':False})
    
        
        
        
        
        