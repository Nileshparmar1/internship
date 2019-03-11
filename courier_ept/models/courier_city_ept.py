from odoo import models, fields


class CourierCityEpt(models.Model):

    _name = 'city.city'

    name = fields.Char(string="City Name", required=True, help="city name")
