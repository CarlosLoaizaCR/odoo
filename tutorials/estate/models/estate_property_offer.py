from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'price must be positive',
    )

    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    property_type_id = fields.Many2one(
            "estate.property.type",
            related="property_id.property_type_id",
            string="Property Type",
            store=True,
        )

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
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                raise UserError("This property already has an accepted offer!")
            
            record.status = 'accepted'
            
            record.property_id.write({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'state': 'offer_accepted',
            })
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True