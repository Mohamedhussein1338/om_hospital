{

    'name': 'HospitalManagement',
    'version': '1.0.0',
    'author': 'mohamed',
    'sequence': -100,
    'website': 'www.proengmht.com',
    'category': 'health',
    'summary': 'Hospital Management System',
    'description': """Hospital Management System """,
    'demo': [],
    'depends': ['product','portal','utm', 'hr','mail'],

    'data': ["security/ir.model.access.csv",
             "views/menuitems.xml",
             "views/appointment.xml",
             "views/res_config_settings_views.xml",
             "views/hr_emp.xml",
             "report/report.xml",
             'report/patient_card.xml'],
    # "views/patient_view.xml"],
    # "views/female_patient_view.xml"],

    # 'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
