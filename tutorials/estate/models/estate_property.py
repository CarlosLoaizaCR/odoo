from odoo import api
from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean()
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    max_offer_price = fields.Float(compute="_compute_max_offer_price", string="Max Offer Price")
    @api.depends("offer_ids.price")
    def _compute_max_offer_price(self):
        for record in self:
            if record.offer_ids:
                record.max_offer_price = max(record.offer_ids.mapped("price"))
            else:
                record.max_offer_price = 0.0


    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False