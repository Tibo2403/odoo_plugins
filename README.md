# Odoo Plugins

This repository contains example Odoo addons.

- `base_plugin`: Minimal plugin demonstrating the basic structure of an Odoo module.
- `social_marketing`: Example plugin for managing social media accounts and posts with scheduling and basic tracking.
- `account_anomaly`: Simple addon for flagging unusual accounting moves.
- `project_prince2`: Manage projects following the PRINCE2 methodology.
- `l10n_be_fiscal_full`: Starter module for Belgian fiscal declarations.
- `l10n_lu_fiscal_full`: Starter module for Luxembourg fiscal declarations.
- Make sure the scheduled action defined in [`social_marketing/data/scheduled_actions.xml`](social_marketing/data/scheduled_actions.xml) is enabled so scheduled posts are processed automatically. You can enable it from **Settings \u2192 Technical \u2192 Automation \u2192 Scheduled Actions** and look for the action with XML ID `social_marketing.ir_cron_social_post`.

## User Manual

For detailed installation and usage instructions, see the [user manual](docs/user_manual.md).

## Installation

1. Copy the addon directories (e.g. `base_plugin`, `social_marketing`, `account_anomaly`, `project_prince2`) into your Odoo `addons_path`.
2. Update the Apps list inside Odoo.
3. Install the desired addon from the Apps menu.

These addons require **Odoo&nbsp;16** for compatibility. See [`social_marketing/__manifest__.py`](social_marketing/__manifest__.py) and [`account_anomaly/__manifest__.py`](account_anomaly/__manifest__.py) for additional module metadata.

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
`odoo.fields` and related modules. This fake Odoo environment allows the addons
to be imported and tested without requiring a real Odoo server. Tests execute
entirely within this simulated setup.
It also defines simple stub models like `ResPartnerBank` used during testing.

### Extending `conftest.py`

Developers can enhance the stub Odoo environment by editing
[`conftest.py`](conftest.py). New field classes or API decorators can be added
to emulate additional framework features that your addons rely on. Extend the
`_Field` base class to create new field types or introduce new decorators under
`odoo.api` as needed.

Example: adding a floating‑point field and a simple decorator::

    class Float(_Field):
        pass

    fields_mod.Float = Float

    def compute(func):
        func._compute = True
        return func

    api_mod.compute = compute

After modifying the stub, run `pytest` locally to ensure the addons and tests
still behave correctly with the new behavior.

## License

This project is licensed under the [MIT License](LICENSE).
