from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique!',
    )

    color = fields.Integer(string="Color", default=0)