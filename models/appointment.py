from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital appointment"
    _rec_name = 'patient_id'  # Understanding Rec Name

    patient_id = fields.Many2one("hospital.pationt", string='Patient',  index=1)
    # patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer('Age', related='patient_id.age')  # related fields
    gender = fields.Selection([('m', "male"), ('f', "female")], string='Gender', related='patient_id.gender')
    notes = fields.Text(string='Registration Notes')
    booking_date = fields.Date(string='Booking Date', required=True)
    appointment_time = fields.Datetime(string='Appointment Time', required=True)
    Priority = fields.Selection([('0', 'Normal'), ('1', 'low'), ('2', 'high'), ('3', 'very high')],
                                string='Priority')  # priority widget
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', ' Cancel')],
        string='Status')  # Add Statusbar
    doctor_id = fields.Many2one("res.users", string="Doctor")
    progress=fields.Integer(string='Progress' , compute='_compute_progress')


    def unlink(self):
        if self.state=='done':
            raise ValidationError(_("error message."))
        return super(HospitalAppointment, self).unlink()

    def actiontest(self):
        return {
            'type':'ir.actions.act_url',
            'url':'https://www.cybrosys.com/blog/types-of-actions-in-odoo-13'
        }


    def action_done(self):
        for rec in self:
            rec.state='done'


    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state=='draft':
                progress=25
            elif rec .state=='in_consultation'  :
                progress=50
            elif rec.state=='done':
                progress=100
            else:
                progress=0
            rec.progress=progress







