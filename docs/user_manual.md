# Odoo Plugins User Manual

This guide explains how to install and operate the example addons provided in this repository. Each section includes a short overview and links to the module README files for more details.

## Installation

1. Copy the desired addon directories into your Odoo `addons_path`.
2. Update the Apps list from the Odoo interface.
3. Install the addons from the Apps menu.

All modules are designed for **Odoo 16**.

## Base Plugin

`base_plugin` is a minimal module demonstrating how to define a basic model, menu items and security rules.

### Usage

1. After installing the module, open **Base Plugin → Base Models**.
2. Create records of `base.plugin.model` and manage them from the list and form views.

For a full explanation of the model and available views, see [base_plugin/README.rst](../base_plugin/README.rst).

## Social Marketing

`social_marketing` provides simple tools to manage social accounts and schedule posts.

### Usage

1. Navigate to **Social Marketing → Configuration → Accounts** and create account records for each platform.
2. Give managers the *Social Marketing Manager* role.
3. Go to **Social Marketing → Posts** to create posts.
4. Choose **Schedule** for future publishing or **Post Now** for immediate publication.

Refer to the [social_marketing/README.rst](../social_marketing/README.rst) for additional configuration notes and an example API integration.

## Account Anomaly

`account_anomaly` flags accounting moves that appear abnormal based on amount thresholds.

### Usage

1. Access **Accounting → Configuration → Anomaly Moves** to create or review moves.
2. Invoke the `find_anomalies` helper method in code to detect unusual records.

See [account_anomaly/README.rst](../account_anomaly/README.rst) for implementation details and examples.

## Belgian Fiscal Declarations

The `l10n_be_fiscal_full` addon offers a skeleton for generating Belgian fiscal declarations.

### Usage

1. Install the module and open **Belgian Fiscal Declarations** in the Odoo menu.
2. Create a new declaration record specifying the declaration type.
3. Use the provided actions to generate XML and mark the declaration as exported.

More background is provided in [l10n_be_fiscal_full/README.rst](../l10n_be_fiscal_full/README.rst).

## Luxembourg Fiscal Declarations

The `l10n_lu_fiscal_full` addon mirrors the Belgian example but targets Luxembourg reporting.

### Usage

1. Install the module and open **Luxembourg Fiscal Declarations** in the Odoo menu.
2. Create a new declaration record specifying the declaration type.
3. Use the provided actions to generate XML and mark the declaration as exported.

See [l10n_lu_fiscal_full/README.rst](../l10n_lu_fiscal_full/README.rst) for details.

