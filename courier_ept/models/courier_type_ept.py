from odoo import models, fields

class CourierTypeEpt(models.Model):

    _name = 'courier.type'
    _rec_name = 'courier_type'

    courier_type = fields.Char(string="Courier type", require=True, help="courier type name")