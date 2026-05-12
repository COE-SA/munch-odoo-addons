{
    'name': 'لوحة التحليل المالي للفروع',
    'version': '1.0.0',
    'category': 'Reporting',
    'summary': 'تحليل مالي شامل لفروع Munch Bakery مع ربط POS',
    'depends': ['base', 'point_of_sale', 'account'],
    'data': [
        'views/menu.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
