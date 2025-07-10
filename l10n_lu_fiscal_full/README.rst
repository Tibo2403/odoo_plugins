Luxembourg Fiscal Declarations
=============================

This addon provides a minimal skeleton for handling Luxembourg fiscal
declarations in Odoo. It defines a single model ``lu.fiscal.declaration``
that can represent different types of filings such as VAT returns,
client listings and other XML exports. Basic eCDF XBRL generation is
included for demonstration purposes.

The ``generate_xml`` method creates a simplistic XML snippet while
``export_xml`` marks the declaration as exported. ``generate_ecdf_xbrl``
and ``export_ecdf`` offer a lightweight example of how an XBRL document
for the eCDF portal could be constructed.

Installation
------------

1. Copy the ``l10n_lu_fiscal_full`` directory into your Odoo addons path.
2. Update the app list and install **Luxembourg Fiscal Declarations** from the
   Apps menu.

Usage Example
-------------

Create and export a simple declaration programmatically::

    declaration = self.env["lu.fiscal.declaration"].create({
        "name": "VAT Return",  # or any other declaration type
    })
    xml = declaration.generate_xml()
    declaration.export_xml()

Generate a sample eCDF XBRL document::

    import json
    data = {
        "1000": 1000,
        "1010": 500,
    }
    declaration = self.env["lu.fiscal.declaration"].create({
        "name": "eCDF", "declaration_type": "xbrl",
        "xbrl_taxonomy": "lu.ecdf.test",
        "account_data": json.dumps(data),
    })
    xml = declaration.generate_ecdf_xbrl()
    declaration.export_ecdf()
