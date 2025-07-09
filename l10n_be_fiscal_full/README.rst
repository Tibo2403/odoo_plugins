Belgian Fiscal Declarations
==========================

This addon provides a minimal skeleton for handling Belgian fiscal
declarations in Odoo. It defines a single model ``be.fiscal.declaration``
that can represent different types of filings such as VAT returns,
client listings, Belcotax forms, ISOC statements and XBRL exports.

The ``generate_xml`` method creates a simplistic XML snippet while
``export_xml`` marks the declaration as exported. The implementation is
intended as a starting point for a complete solution that would follow
official specifications and integrate with Intervat, Belcotax or Biztax.

Installation
------------

1. Copy the ``l10n_be_fiscal_full`` directory into your Odoo addons path.
2. Update the app list and install **Belgian Fiscal Declarations** from the
   Apps menu.

Usage Example
-------------

Create and export a simple declaration programmatically::

    declaration = self.env["be.fiscal.declaration"].create({
        "name": "VAT Return",  # or any other declaration type
    })
    xml = declaration.generate_xml()
    declaration.export_xml()
