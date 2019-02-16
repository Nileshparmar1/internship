from odoo import fields,models

class resPartner(models.Model):

    _inherit='res.partner'
    
    fax=fields.Char(string="Fax",help="Fax")
    linkedin_id=fields.Char(string="Linkedin",help="Linkedin")
    
    
    
    