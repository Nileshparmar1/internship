from odoo import models, fields


class CourierDeliveryEpt(models.Model):

    _name = 'courier.delivery'
    _rec_name = 'courier_id'

    courier_id = fields.Many2one('courier.courier', required=True, string="Name")
    type = fields.Selection([
        ('standard courier service', 'Standard Courier Service'),
        ('overnight service', 'Overnight Service'),
        ('same day express courier', 'Same Day Express Courier')
        ], default='standard courier service', required=True, help="courier service type")
    courier_line = fields.One2many('courier.charges.line', 'courier_delivery_id',
                                   string="Courier line", auto_join=True)


class CourierChargesLine(models.Model):

    _name = 'courier.charges.line'

    courier_delivery_id = fields.Many2one('courier.delivery', string="Courier reference",
                                          require=True)
    country_id = fields.Many2one('res.country', string='Country')
    from_weight = fields.Float(string="From Weight", help="weight of courier package")
    to_weight = fields.Float(string="To Weight", help="weight of courier package")
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    courier_amount = fields.Float(string="Amount", require=True, help="amount of courier")
