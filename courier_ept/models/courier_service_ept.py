from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import Warning


class CourierServiceEpt(models.Model):

    _name = 'courier.service'

    @api.multi
    def calculate_expected_date(self):
        """ this method is used to get expected date """
        self.update({
            'Expected_delivery_date':fields.Datetime.now() + timedelta(hours=self.hours)
            })
        
    @api.depends('package_weight', 'courier_id')
    def _calculate_charge(self):
        """
        This method is used to get calculated amount on change of courier id or weight of courier.
        """
        res = self.env['courier.delivery'].search([('courier_id', '=', self.courier_id.id)])
        lines = res.courier_line
        
        for line in lines:
            if self.package_weight >= line.from_weight and self.package_weight <= line.to_weight:
                self.update({'amount':line.courier_amount})
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       index=True, default='New')
    courier_id = fields.Many2one('courier.courier', string="Name",
                                 required=True, help="courier name")
    receiver = fields.Many2one('courier.res.partner', string="Assign To",
                               required=True, help="courier receiver name")
    sender = fields.Many2one('courier.res.partner', string="Sender",
                             required=True, help="courier sender name")
    courier_description = fields.Text(string="Description", help="courier description")
    state = fields.Selection([
        ('draft', 'New'),
        ('return', 'Return'),
        ('delivered', 'Delivered'),
        ('cancel', 'Cancel')
        ], string='Status', readonly=True, copy=False, index=True, \
        track_visibility='onchange', track_sequence=3, default='draft')
    courier_type = fields.Many2one('courier.type', string="Type",
                                   require=True, help="courier type name")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    zip = fields.Char('Zip', change_default=True)
    country_id = fields.Many2one('res.country', string='Country')
    company_name = fields.Many2one('res.company', string='Company')
    package_weight = fields.Float(string="Weight", help="weight of courier")
    distance = fields.Float(string="Kilometer", related='route_id.total_distance',
                            store=True, help="kilometer of source to destination place")
    # amount = fields.Float(string="Courier Charge", help="amount of courier")
    amount = fields.Float(string="Courier Charge", compute='_calculate_charge', help="amount of courier")
    route_id = fields.Many2one('route.route', string="Route Name",
                               require=True, help="route name")
    hours = fields.Float(string="Expected Delivery Date", related='route_id.calculated_hours')
    Expected_delivery_date = fields.Datetime(string="Expected Delivery Date",
                                             compute='calculate_expected_date',
                                             help="delivery date of courier")
    delivered_date = fields.Datetime(string="Delivered Date", readonly=True, help="courier delivered date")
    return_reason = fields.Char(string="Return Reason", readonly=True, help="return reason")
    return_date = fields.Datetime(string="Return Date", readonly=True, help="return courier date")
    delivery_method = fields.Many2one('delivery.carrier', string="Delivery Method", help="delivery method")
    delivery_price = fields.Float(string="Delivery Price", help="delivery price")

    @api.model
    def create(self, vals):
        '''
        @func: this function is used to create courier service no.
        '''
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('courier.service') or 'New'
        return super(CourierServiceEpt, self).create(vals)
    
    @api.multi
    def action_delivered(self):
        """ this method is used to write state in delivered and current date-time """
        return self.write({
            'state':'delivered',
            'delivered_date':fields.Datetime.now()
            })

    @api.multi
    def action_cancel(self):
        """ this method is used to write state in cancel """
        return self.write({'state':'cancel'})

    @api.multi
    def action_return(self):
        """ this method is used to write state in return and set delivered date false """
        self.write({'state':'return', 'return_date':fields.Datetime.now()})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.return',
            'views':[[self.env.ref('courier_ept.courier_return_wizard_form').id, 'form']],
            'target': 'new',
        }

    @api.multi
    def action_draft(self):
        """ this method is used to write state in draft """
        return self.write({'state':'draft',
                           'delivered_date':False,
                           })

    @api.onchange('package_weight', 'courier_id')
    def _onchange_amount(self):
        """
        This method is used to get calculated amount on change of courier id or weight of courier.
        """
        res = self.env['courier.delivery'].search([('courier_id', '=', self.courier_id.id)])
        lines = res.courier_line
        max_weight = 0
        for line in lines:
            if max_weight < line.to_weight:
                max_weight = line.to_weight

        if self.package_weight < 0 or self.package_weight > max_weight:
            raise Warning("Our maximum weight for items is %d" % max_weight)

    @api.onchange('delivery_method', 'package_weight')
    def _onchange_delivery_method(self):
        carriers = self.env['delivery.carrier'].search([('id', '=', self.delivery_method.id)])
        lines = carriers.price_rule_ids
        for line in lines:
            operator = line.operator
            if['package_weight', operator, line.max_value]:
                price = line.list_base_price + line.list_price * self.package_weight
                self.update({'delivery_price':price})
        
    @api.multi
    def action_print(self):
        """ this method is used to print courier """
        return self.env.ref('courier_ept.action_report_courier')\
            .with_context({'discard_logo_check': True}).report_action(self)
