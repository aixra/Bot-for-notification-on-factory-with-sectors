from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

import config


def load_catalog() -> dict[str, list[str]]:
    path = Path(config.EQUIPMENT_EXCEL_FILE)
    if not path.exists():
        return {k: list(v) for k, v in config.DEFAULT_DEVICES.items()}

    workbook = load_workbook(path, data_only=True)
    sheet_name = config.EQUIPMENT_SHEET_NAME
    sheet = workbook[sheet_name] if sheet_name in workbook.sheetnames else workbook.active

    catalog: dict[str, list[str]] = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row:
            continue
        sector = str(row[0]).strip() if row[0] is not None else ""
        device = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
        if not sector or not device:
            continue
        catalog.setdefault(sector, [])
        if device not in catalog[sector]:
            catalog[sector].append(device)

    return catalog if catalog else {k: list(v) for k, v in config.DEFAULT_DEVICES.items()}
