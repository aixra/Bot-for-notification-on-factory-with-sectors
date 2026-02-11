from __future__ import annotations

from pathlib import Path

import config


def get_next_request_id() -> int:
    counter_path = Path(config.REQUEST_ID_COUNTER_FILE)
    if not counter_path.exists():
        counter_path.write_text("1", encoding="utf-8")
        return 0

    raw_value = counter_path.read_text(encoding="utf-8").strip()
    current = int(raw_value) if raw_value.isdigit() else 0
    counter_path.write_text(str(current + 1), encoding="utf-8")
    return current
