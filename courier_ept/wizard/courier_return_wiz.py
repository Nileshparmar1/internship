from odoo import fields, models, api

class CourierReturn(models.TransientModel):
    
    _name='courier.return'
    
    name=fields.Char(string="Reason",help="courier return reason")
    
    @api.multi
    def set_return_reason(self):
        
        context = dict(self._context) or {}
        courier_id = self.env['courier.service'].browse(context.get('active_id', False))
        courier_id.update({'return_reason':self.name})