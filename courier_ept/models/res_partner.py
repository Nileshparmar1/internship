from odoo import models, fields

class ResPartner(models.Model):

    _name = 'courier.res.partner'

    name = fields.Char(string="Name", require=True, help="partner name")