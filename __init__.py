# -*- coding: utf-8 -*-
import json
from odoo import api
from odoo.modules.module import get_module_resource 

from . import controllers
from . import models
from . import wizard


def _load_json_data(cr, registry):

    print(" load json ")

    json_file_path = get_module_resource('jt_gs1_gtin', 'static/', 'v20230605_EN.json')
    with open(json_file_path) as f:
        data = json.load(f)
        test = 1