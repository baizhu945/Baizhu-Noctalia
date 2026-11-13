#!/usr/bin/env python3
"""Schedule a layout when the tray drawer rebuilds its icons.

v5.4 indexes an SNI IconThemePath on a worker. The first unfold after a long
idle misses that cache and rebuilds when the scan finishes. The drawer requests
only an update for that rebuild. Layout invalidation raised during the frame is
ignored, and the paint then clears the dirty flag, so every new icon stays at
the origin. v5.1 resolved the same paths synchronously inside layout.
"""

from pathlib import Path

path = Path("src/shell/tray/tray_drawer_panel.cpp")
text = path.read_text()
old = """  m_drawerWidget->setUpdateCallback([]() { PanelManager::instance().requestUpdateOnly(); });
"""
new = """  // Replacing the icon grid is structural. An update-only frame ignores the layout
  // invalidation raised by those new nodes, so they stay stacked at the origin.
  m_drawerWidget->setUpdateCallback([]() {
    PanelManager::instance().requestUpdateOnly();
    PanelManager::instance().requestLayout();
  });
"""
if text.count(old) != 1:
    raise SystemExit(f"tray drawer update callback changed upstream: found {text.count(old)}")
path.write_text(text.replace(old, new))
