Base Plugin
===========

This addon provides a minimal structure for creating a custom Odoo module.

Main Files
----------

- ``models/base_model.py`` - defines the ``base.plugin.model`` with a single
  ``name`` field.
- ``views/base_model_views.xml`` - tree and form views plus the menu entries for
  accessing records of the model.
- ``security/ir.model.access.csv`` - grants basic CRUD access to internal
  users.

Menu Items
----------

The view definition adds a small menu under **Base Plugin**:

1. **Base Plugin** – top‑level application menu.
2. **Base Model** – submenu grouping related actions.
3. **Base Models** – opens the list/form views of ``base.plugin.model`` using
   the ``action_base_model`` window action.

Usage Example
-------------

Creating a record programmatically::

    self.env["base.plugin.model"].create({"name": "My Record"})

To extend the model in another module::

    from odoo import models, fields

    class ExtendedModel(models.Model):
        _inherit = "base.plugin.model"

        description = fields.Text()

