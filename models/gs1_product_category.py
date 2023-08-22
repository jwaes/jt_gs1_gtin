from odoo import api, fields, models, _



class GPCSegment(models.Model):
    _name = "jt.gs1.segment"
    _description = "GS1 GPC segment"
    _order = "code"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )

    definition = fields.Char(
        string="Definition",
        translate=True,
    )

    code = fields.Char(
        string='Code',
        indexed=True,
        required=True,
    )

    active = fields.Boolean('active', default=True)

    family_ids = fields.One2many('jt.gs1.family', 'segment_id', string='GS1 Families')

    @api.constrains('code')
    def _check_code(self):
        for segment in self:
            recs = self.search_count([('code', '=', segment.code)])
            if recs > 1:
                raise ValidationError(_(
                    'The code of the segment must be unique.'))

class GPCFamily(models.Model):
    _name = "jt.gs1.family"
    _description = "GS1 GPC family"
    _order = "code"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )

    definition = fields.Char(
        string="Definition",
        translate=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    active = fields.Boolean('active', default=True)

    segment_id = fields.Many2one('jt.gs1.segment', string='GS1 Segment')

    classes_ids = fields.One2many('jt.gs1.class', 'family_id', string='GS1 Classes')

    @api.constrains('code')
    def _check_code(self):
        for family in self:
            recs = self.search_count([('code', '=', family.code)])
            if recs > 1:
                raise ValidationError(_(
                    'The code of the family must be unique.'))

class GPCClass(models.Model):
    _name = "jt.gs1.class"
    _description = "GS1 GPC class"
    _order = "code"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )

    definition = fields.Char(
        string="Definition",
        translate=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    active = fields.Boolean('active', default=True)

    family_id = fields.Many2one('jt.gs1.family', string='GS1 Family')

    brick_ids = fields.One2many('jt.gs1.brick', 'class_id', string='GS1 bricks')

    @api.constrains('code')
    def _check_code(self):
        for klas in self:
            recs = self.search_count([('code', '=', klas.code)])
            if recs > 1:
                raise ValidationError(_(
                    'The code of the class must be unique.'))

class GPCBrick(models.Model):
    _name = "jt.gs1.brick"
    _description = "GS1 GPC brick"
    _order = "code"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )

    definition = fields.Char(
        string="Definition",
        translate=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    active = fields.Boolean('active', default=True)

    class_id = fields.Many2one('jt.gs1.class', string='GS1 Class')

    full_name = fields.Char(compute='_compute_full_name', string='Display name')
    
    @api.depends('class_id', 'name')
    def _compute_full_name(self):
        for brick in self:
            brick.full_name = brick.class_id.family_id.segment_id.name + " > " + brick.class_id.family_id.name + " > " + brick.class_id.name + " > " + brick.name

    @api.constrains('code')
    def _check_code(self):
        for brick in self:
            recs = self.search_count([('code', '=', brick.code)])
            if recs > 1:
                raise ValidationError(_(
                    'The code of the brick must be unique.'))                    
