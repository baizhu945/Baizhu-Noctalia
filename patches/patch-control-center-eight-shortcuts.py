#!/usr/bin/env python3
"""Allow eight Control Center Home shortcuts without changing the native default list."""

from pathlib import Path

changes = {
    "src/shell/control_center/tabs/home_tab.cpp": (
        "const std::size_t count = std::min(shortcuts.size(), std::size_t{6});",
        "const std::size_t count = std::min(shortcuts.size(), std::size_t{8});",
    ),
    "src/shell/settings/settings_registry.cpp": (
        ".items = cfg.controlCenter.shortcuts, .suggestedOptions = controlCenterShortcutOptions(cfg), .maxItems = 6",
        ".items = cfg.controlCenter.shortcuts, .suggestedOptions = controlCenterShortcutOptions(cfg), .maxItems = 8",
    ),
}

for filename, (old, new) in changes.items():
    path = Path(filename)
    text = path.read_text()
    if text.count(old) != 1:
        raise SystemExit(f"{filename}: expected one shortcut limit, found {text.count(old)}")
    path.write_text(text.replace(old, new))
