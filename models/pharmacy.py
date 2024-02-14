from  odoo import models,fields,api





class AppointmentPharmacy(models.Model):
    _name="appointment.pharmacy"
    _description=" appointment Pharmacy"

#related="product_id.list_price",
    product_id=fields.Many2one('product.product', string='Product', required=True)
    price=fields.Float(related="product_id.list_price", string="Price")
    qty=fields.Integer(string="Quantity" ,default=1)
    appointment_id=fields.Many2one("hospital.pationt" ,string="Patient")
    doctors_id=fields.Many2many("res.partner",string="doctor")
    total_price = fields.Monetary(string='Total Price', compute='_compute_total_price',  currency_field='currency_id',store=True)
    currency_id=fields.Many2one('res.currency' ,related='company_id.currency_id', string='currency')
    company_id = fields.Many2one('res.company',  default=lambda self: self.env.user.company_id.id,
                                 index=1)
    reference_record=fields.Reference(selection=[('hospital.pationt','pationt'),('hospital.appointment','Appointment')],string='record')



    @api.depends('qty', 'price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.qty * record.price




