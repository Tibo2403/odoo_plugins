# Odoo Plugins

This repository contains example Odoo addons.

- `base_plugin`: Minimal plugin demonstrating the basic structure of an Odoo module.
- `social_marketing`: Example plugin for managing social media accounts and posts with scheduling and basic tracking.

## Installation

1. Copy the addon directories (e.g. `base_plugin`, `social_marketing`) into your Odoo `addons_path`.
2. Update the Apps list inside Odoo.
3. Install the desired addon from the Apps menu.

These addons target **Odoo&nbsp;16**, as specified in each `__manifest__.py` file.

## Running tests

1. Install the test requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Execute the tests using `pytest`:

   ```bash
   pytest
   ```

### Test Environment

The `conftest.py` file provides mocked versions of `odoo.models`,
`odoo.fields` and related modules. This lightweight stub allows the addons to
be imported and tested without requiring a real Odoo server. Tests execute
entirely with the simulated environment created in this file.
