from odoo import models, fields, api


class CourierRouteEpt(models.Model):

    _name = 'route.route'

    @api.depends('route_line.distance')
    def _calculate_distance(self):
        """ this method to calculate hours of courier route line. """
        for route in self:
            total_kilometer = 0.0
            for line in route.route_line:
                total_kilometer += line.distance
            route.update({'total_distance': total_kilometer})

    @api.depends('route_line.hours')
    def _calculate_hours(self):
        """ this method is used to get sum of courier line hours. """
        for route in self:
            total_hours = 0.0
            for line in route.route_line:
                total_hours += line.hours
            route.update({'calculated_hours':total_hours})

    name = fields.Char(string="name", required=True, help="route name")
    route_line = fields.One2many('courier.route.line', 'route_id',
                                 string="Route Line", auto_join=True)
    total_distance = fields.Float(string="Total Hours",
                                  compute='_calculate_distance', help="total kilo-meter")
    calculated_hours = fields.Float(string="Total_hours",
                                    compute='_calculate_hours', help="total hours")


class CourierRouteLine(models.Model):

    _name = "courier.route.line"
    _rec_name = "distance"

    route_id = fields.Many2one('route.route', string="route reference", required=True)
    from_city = fields.Many2one('city.city', string="From City", required=True)
    to_city = fields.Many2one('city.city', string="To City", required=True)
    distance = fields.Float(string="Distance", required=True)
    hours = fields.Float(string="Hours", required=True)
