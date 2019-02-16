{
    'name': 'Sales Extend',
    'version': '1.1',
    'category': 'Sales',
    'summary': 'Sales internal machinery',
    'description': """
This module contains all the common features of Sales Management and eCommerce.
    """,
    'website':'www.emoprotechnologies.com',
    'author':'Nilesh Parmar',
    'depends': ['sale'],
    'data': [
        'views/res_partner.xml',
        'views/sale_order_view.xml'
    ],
    'installable': True,
    'application':True,
    'auto_install': False
}
