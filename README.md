# Odoo Plugins

This repository contains example Odoo addons.

- `base_plugin`: Minimal plugin demonstrating the basic structure of an Odoo module.
- `social_marketing`: Example plugin for managing social media accounts and posts with scheduling and basic tracking.
- Make sure the scheduled action defined in [`social_marketing/data/scheduled_actions.xml`](social_marketing/data/scheduled_actions.xml) is enabled so scheduled posts are processed automatically.

## Installation

1. Copy the addon directories (e.g. `base_plugin`, `social_marketing`) into your Odoo `addons_path`.
2. Update the Apps list inside Odoo.
3. Install the desired addon from the Apps menu.

These addons require **Odoo&nbsp;16** for compatibility. See [`social_marketing/__manifest__.py`](social_marketing/__manifest__.py) for additional module metadata.

## Running tests

1. Install the test requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Execute the tests using `pytest`:

   ```bash
   pytest
   ```
