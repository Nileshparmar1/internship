# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{	
    'name':'Courier Ept',
    'version':'12.0.1.0',
    'category':'service',
    'sequence':3,
    'description':"""
    this module contains all the common feature of courier system and keep track the courier
    """,
    'summary':'Courier Information',
    'web':'www.emiprotechnologies.com',
    'data':['views/courier_service_view.xml',
            'views/courier_ept_view.xml',
            'views/courier_delivery_view.xml',
            'views/courier_config_view.xml',
            'views/courier_city_view.xml',
            'views/res_partner_view.xml',
            'views/courier_type_view.xml',     
            'report/courier_report.xml',
            'report/courier_template.xml',
            'wizard/courier_return_wiz.xml',
            'data/ir_sequence_courier.xml',
            'security/ir.model.access.csv'
    ],
    'depends':['base'],
    'installable':True,
    'auto_install':False,
    'application':True,
}
