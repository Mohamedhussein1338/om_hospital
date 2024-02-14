from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo import _
from odoo.osv import expression


class HospitalPationts(models.Model):
    _name = "hospital.pationt"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _inherits = {'hr.employee': 'original_hr_employee_id'}

    _descriptin = "Hospitsl Pationts"

    name = fields.Char(string='Name', required=True, tracking=1)


    birth_date = fields.Date(tracking=3)
    age = fields.Integer(string="Age", compute="_compute_age", store=True ,tracking=True)
    company_id = fields.Many2one('res.company', string='Hospital', default=lambda self: self.env.user.company_id.id,
                                 index=1)
    original_hr_employee_id = fields.Many2one('hr.employee', string='Original HR Employee', required=True, ondelete='cascade')


    # age=fields.Integer(string='Age' ,tracking=True)
    address = fields.Text(tracking=4)
    reference=fields.Text(string="Reference")
    gender = fields.Selection([('m', "male"), ('f', "female")], string='Gender')
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary(tracking=5)
    cv = fields.Html()
    login_time = fields.Datetime()
    pharmacy_id = fields.One2many("appointment.pharmacy", 'appointment_id', string="Pharmacy" ,tracking=10)
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    active = fields.Boolean("Active", default=True)
    job_title = fields.Char(string='Job Title')
    category_ids = fields.Many2many('res.company', string='Categories')
    work_email = fields.Char(string='Work Email')
    work_phone = fields.Char(string='Work Phone')
    user_id = fields.Many2one('res.users', string='User')







    # use name_get
    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            if rec.name:
                name = '%s %s' % (rec.reference, name)
            result.append((rec.id, name))
        return result

    # name-search

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = args + ['|', ('age', operator, name), ('address', operator, name)]

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # some of orm methodes
    #         groups = self.Model.read_group([], fields=['state', 'value'], groupby=['state'])
    def orm_methods(self):
        for rec in self:
            patients = self.env['hospital.pationt'].search([])  # search methode
            print('the search run', patients)
            print('map run', patients.mapped('company_id'))
            print('sorted run ', patients.sorted(key=lambda r: r.name))
            patientes = self.env['hospital.pationt'].search_count([])  # search _count methode
            print('search count', patientes)
            browse_method = self.env['hospital.pationt'].browse(patients)  # browse methode
            print('browse run', browse_method)
            read_group_method= self.env['hospital.pationt'].read_group([('age','>','20')], fields=['name'], groupby=['age'])
            print('the read group run', read_group_method)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     """ Returns a list of tuples containing id, name, as internally it is called {def name_get}
    #         result format: {[(id, name), (id, name), ...]}
    #     """
    #     args = args or []
    #     if operator == 'ilike' and not (name or '').strip():
    #         domain = []
    #     else:
    #         connector = '&' if operator in expression.NEGATIVE_TERM_OPERATORS else '|'
    #         domain = [connector, ('age', operator, name), ('address', operator, name)]
    #     return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    # python constraints
    @api.constrains('birth_date')
    def _check_birth_data(self):
        for rec in self:
            if rec.birth_date and rec.birth_date > fields.Date.today():
                raise ValidationError(_('the entered birth_date is not accepted.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_check_home_action(self):
        for rec in self:
            if rec.pharmacy_id:
                raise ValidationError(_("NO"))

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        sup = super(ResUsers, self)
        if not default or not default.get('email'):
            # avoid sending email to the user we are duplicating
            sup = super(ResUsers, self.with_context(no_reset_password=True))
        return sup.copy(default=default)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    @api.model
    def create(self, record):
        record['reference'] = self.env['ir.sequence'].next_by_code('patient.sequence')
        return super(HospitalPationts, self).create(record)



    # computed fields
    @api.depends('birth_date')
    def _compute_age(self):
      for record in self:
        if record.birth_date:
            dob = fields.Date.from_string(record.birth_date)
            today = fields.Date.today()
            age = relativedelta(today, dob).years
            record.age = age
        else:
            record.age = 0


    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    def open_patient_appointment(self):
        return

