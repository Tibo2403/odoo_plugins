Belgian Fiscal Declarations
==========================

This addon provides a minimal skeleton for handling Belgian fiscal
declarations in Odoo. It defines a single model ``be.fiscal.declaration``
that can represent different types of filings such as VAT returns,
client listings, Belcotax forms, ISOC statements and XBRL exports.

The ``generate_xml`` method originally created a simplistic XML snippet
while ``export_xml`` merely flagged the declaration as exported. The
model now provides basic fields for common Intervat VAT codes (00, 01,
54…), intra‑EU operations and period information. ``generate_xml``
produces a small ``<VATDeclaration>`` document using these values.
This remains a lightweight example; a full solution would follow the
official specifications and integrate with Intervat, Belcotax or Biztax.

BNB/CBN XBRL
------------

This version includes a lightweight example for generating corporate tax
XBRL files. New fields ``xbrl_taxonomy`` and ``account_data`` store the
taxonomy name and account balances in JSON. ``generate_bnb_xbrl`` produces
a simple XBRL snippet while ``export_bnb`` marks the declaration as
exported.

Belcotax 281.x
---------------

The module now includes a basic ``belcotax.declaration`` model used by the
export wizard. A declaration stores the fiscal year, form type and partner
information. The wizard generates a tiny XML snippet and returns it as a
downloadable file. This is only a demonstration of the export flow and does
not attempt to implement the official XSD.

Installation
------------

1. Copy the ``l10n_be_fiscal_full`` directory into your Odoo addons path.
2. Update the app list and install **Belgian Fiscal Declarations** from the
   Apps menu.

Usage Example
-------------

Create and export a simple declaration programmatically::

    declaration = self.env["be.fiscal.declaration"].create({
        "name": "VAT Return",
        "declaration_type": "vat",
        "vat_code_00": 100,
        "vat_code_01": 50,
        "period_type": "month",
        "period_month": "3",
    })
    xml = declaration.generate_xml()
    declaration.export_xml()

Generate a sample BNB XBRL document::

    import json
    data = {
        "100": 1000,
        "101": 500,
    }
    declaration = self.env["be.fiscal.declaration"].create({
        "name": "BNB", "declaration_type": "xbrl",
        "xbrl_taxonomy": "be.bnb.test",
        "account_data": json.dumps(data),
    })
    xml = declaration.generate_bnb_xbrl()
    declaration.export_bnb()
