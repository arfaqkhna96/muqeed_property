{
    'name': 'Muqeed Property',
    'version': '1.0.1',
    'description': 'Estate',
    'author': 'S P Muqeed',
    'category': 'Bussiness',
    'license': 'LGPL-3',
    'sequence': '-100',
    'depends':[
        'base','web','portal','mail'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/agent_form.xml',
        'views/my_property.xml',
        'views/my_property_templates.xml',
        'views/template.xml',
        'views/property_detail_template.xml',
        'views/agent_property_views.xml',
        'views/email_template.xml',
        'views/form_template.xml',
        'views/menu.xml',

    ],

    'Installable': True,
    'application': True,
}
