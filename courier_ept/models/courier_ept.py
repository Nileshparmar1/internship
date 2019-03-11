from odoo import models, fields, api


class CourierEpt(models.Model):

    _name = 'courier.courier'
    name = fields.Char(string="Name", required=True, help="Courier name")
    courier_code = fields.Integer(string="Code", help="courier code")

    @api.multi
    @api.depends('name', 'courier_code')
    def name_get(self):
        """ this method used to get courier name and code in list of tuple. """
        result = []
        for courier in self:
            name = courier.name + ' - ' + str(courier.courier_code)
            result.append((courier.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """ this method used to search from available record of courier """
        domain = ['|', ('courier_code', operator, name), ('name', operator, name)]
        courier_codes = self._search(domain, args, limit=limit, access_rights_uid=name_get_uid)
        return self.browse(courier_codes).name_get()
