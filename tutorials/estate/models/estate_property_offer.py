from dateutil.relativedelta import relativedelta
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", store=True, inverse="_inverse_date_deadline")
    
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date_start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date_start + relativedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
            for record in self:
                date_start = record.create_date.date() if record.create_date else fields.Date.today()
                if record.date_deadline:
                    record.validity = (record.date_deadline - date_start).days
