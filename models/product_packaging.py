import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    product_packaging_sequence = fields.Integer('Product Packaging Sequence', default=1)

    _sql_constraints = [(
        'unique_product_packaging_sequence',
        'unique(product_id, product_packaging_sequence)',
        'The combination product_packaging_sequence/product must be unique.'),(
        'unique_product_packaging_barcode',
        'unique(barcode)',
        'The product_packaging barcode must be unique')]

    @api.model
    def create(self, vals):
        # _logger.info(vals)
        packagings = self.env['product.packaging'].search([('product_id.id' ,'=', vals['product_id'])])
        # _logger.info(packagings)
        highest_seq = 1

        if len(packagings) > 0:
            for pack in packagings:
                if pack.product_packaging_sequence > highest_seq:
                    highest_seq = pack.product_packaging_sequence            
            vals['product_packaging_sequence'] = highest_seq + 1
        else :
             vals['product_packaging_sequence'] = 1
        parent = self.env['product.product'].browse(vals['product_id'])
        if parent.barcode:
            bc = self._get_barcode(parent.barcode, vals['product_packaging_sequence'])
            if bc:
                vals['barcode'] = bc

        res = super(ProductPackaging, self).create(vals)
        return res

    @api.depends('product_id', 'product_id.barcode', 'product_packaging_sequence')
    def generate_gtin14(self):
        _logger.info("called generate gtin14")
        for pp in self:
            _logger.info(pp.product_id.barcode)
            if pp.product_id.barcode and len(pp.product_id.barcode) == 13:
                pp.barcode = self._get_barcode(pp.product_id.barcode, pp.product_packaging_sequence)


    def _get_barcode(self, parent_code, sequence_code):
        if len(parent_code) != 13:
            _logger.error("product GTIN should be of length 13")
            return None
        if sequence_code > 8:
            _logger.error("We are out of logistics sequence numbers to create a GTIN14")
            return None
        code = str(parent_code[:-1])
        base = str(sequence_code) + code
        checksum = self._gtin_checksum(base)
        bc = base + str(checksum)
        _logger.info("new gtin14 barcode is %s", bc)
        return bc

    def _gtin_checksum(self, code):
        total = 0

        for (i, c) in enumerate(code):
            if i % 2 == 1:
                total = total + (3 * int(c))
            else:
                total = total + int(c)

        check_digit = (10 - (total % 10)) % 10
        return check_digit            