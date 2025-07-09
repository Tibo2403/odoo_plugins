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
