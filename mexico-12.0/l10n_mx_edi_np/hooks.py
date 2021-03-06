# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from lxml import etree, objectify

from odoo import SUPERUSER_ID, api
from odoo.addons.l10n_mx_edi.hooks import _load_xsd_files


def post_init_hook(cr, registry):
    url = 'http://www.sat.gob.mx/sitio_internet/cfd/notariospublicos/notariospublicos.xsd' # noqa
    namespaces = 'http://www.sat.gob.mx/notariospublicos'
    _load_xsd_complement(cr, registry, url, namespaces)


def _load_xsd_complement(cr, registry, url, namespaces):
    db_fname = _load_xsd_files(cr, registry, url)
    env = api.Environment(cr, SUPERUSER_ID, {})
    xsd = env.ref('l10n_mx_edi.xsd_cached_cfdv33_xsd', False)
    if not xsd:
        return False
    complement = {
        'namespace': namespaces,
        'schemaLocation': db_fname,
    }
    node = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
                         complement)
    res = objectify.fromstring(base64.decodebytes(xsd.datas))
    res.insert(0, node)
    xsd_string = etree.tostring(res, pretty_print=True)
    xsd.datas = base64.encodebytes(xsd_string)
    return True
