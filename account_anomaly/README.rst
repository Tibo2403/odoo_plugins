Accounting Anomaly Plugin
=========================

This addon provides a simple model for storing accounting moves and helper
functions to detect unusual entries.  A move is considered anomalous when
its amount is negative or exceeds a configurable threshold (default 10,000).

Main Files
----------

- ``models/account_move.py`` – defines ``account.anomaly.move`` with a few
  basic fields and anomaly detection logic.
- ``views/account_move_views.xml`` – example tree and form views so records
  can be managed from the Odoo interface.
- ``security/ir.model.access.csv`` – grants CRUD access to internal users.

Usage Example
-------------

Detect anomalies programmatically::

    AccountMove.find_anomalies(threshold=5000.0)
