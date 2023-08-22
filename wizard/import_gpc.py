import logging
import mimetypes
import base64

import xml.etree.ElementTree as ET

from odoo import fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ImportGPC(models.TransientModel):
    _name = 'jt.import.gpc'
    _description = 'Import GS1 Global Categories from json file'

    file = fields.Binary()

    def action_import(self):
        self.ensure_one()
        _logger.info("About to import")

        file_content = base64.decodebytes(self.file)
        file_content = file_content.decode("utf-8")

        root = ET.fromstring(file_content)

        languageCode = root.get('languageCode').lower()

        for segment_node in root:
            if segment_node.tag != "segment":
                raise UserError("Expected segment but found ", segment_node.tag)

            vals = {
                'name': segment_node.get('text'),
                'code': segment_node.get('code'),
                'active': segment_node.get('active'),
            }
            segment = self.env['jt.gs1.segment'].search([
                    ('code', '=', segment_node.get('code')),
                ])
            if not segment:
                self.env['jt.gs1.segment'].create(vals)
            else :
                segment.write(vals)

            _logger.info(segment_node.tag + " {" + str(segment.id) + "}[" + segment.code + "] " + segment.name)
            
            for family_node in segment_node:
                if family_node.tag != "family":
                    raise UserError("Expected family but found ", family_node.tag)
                vals = {
                    'name': family_node.get('text'),
                    'code': family_node.get('code'),
                    'active': family_node.get('active'),
                    'segment_id': segment.id,
                }
                family = self.env['jt.gs1.family'].search([
                        ('code', '=', family_node.get('code')),
                    ])
                if not family:
                    self.env['jt.gs1.family'].create(vals)
                else :
                    family.write(vals)

                _logger.info(family_node.tag + " {" + str(family.id) + "}[" + family.code + "] " + family.name + "[parent:" + str(family.segment_id.id) + "]")                 

                for class_node in family_node:
                    if class_node.tag != "class":
                        raise UserError("Expected class but found ", class_node.tag)
                    vals = {
                        'name': class_node.get('text'),
                        'code': class_node.get('code'),
                        'active': class_node.get('active'),
                        'family_id': family.id,
                    }
                    klass = self.env['jt.gs1.class'].search([
                            ('code', '=', class_node.get('code')),
                        ])
                    if not klass:
                        self.env['jt.gs1.class'].create(vals)
                    else :
                        klass.write(vals)         

                    for brick_node in class_node:
                        if brick_node.tag != "brick":
                            raise UserError("Expected brick but found ", brick_node.tag)
                        vals = {
                            'name': brick_node.get('text'),
                            'code': brick_node.get('code'),
                            'active': brick_node.get('active'),
                            'class_id': klass.id,
                        }
                        brick = self.env['jt.gs1.brick'].search([
                                ('code', '=', brick_node.get('code')),
                            ])
                        if not brick:
                            self.env['jt.gs1.brick'].create(vals)
                        else :
                            brick.write(vals)                                        
                

        # data = json.loads(file_content) 


        # for iterator in data:
        #     _logger.info(iterator, ":", data[iterator])
