import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange('barcode', 'packaging_ids')
    def barcode_change(self):
        _logger.info("called barcode change")
        for p in self:
            for pp in p.packaging_ids:
                pp.generate_gtin14()
