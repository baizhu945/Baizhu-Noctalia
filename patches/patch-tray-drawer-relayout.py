#!/usr/bin/env python3
"""Lay tray icons out again after an update-phase rebuild.

v5.4 indexes an SNI IconThemePath on a worker. The drawer does not open that
index until it is unfolded, so the first unfold after a long idle misses the
cache, paints fallbacks, and rebuilds when the scan finishes. That rebuild runs
from an update-only frame. Layout invalidation raised during the frame is
ignored, and the paint then clears the dirty flag, leaving every new icon at
the origin. v5.1 resolved the same paths synchronously inside layout.
"""

from pathlib import Path

path = Path("src/shell/bar/widgets/tray_widget.cpp")
text = path.read_text()
old = """void TrayWidget::doUpdate(Renderer& renderer) {
  syncState(renderer);
  if (m_rebuildPending) {
    rebuild(renderer);
    m_rebuildPending = false;
  }
"""
new = """void TrayWidget::doUpdate(Renderer& renderer) {
  syncState(renderer);
  if (m_rebuildPending) {
    rebuild(renderer);
    m_rebuildPending = false;
    // Rebuild replaces the icon nodes. The surrounding frame is update-only, so
    // the layout dirty flag it raises is dropped and the icons stay stacked.
    if (m_container != nullptr) {
      m_container->setGap(resolvedInlineEntryGap());
      m_container->layout(renderer);
      layoutHoverOverlays();
    }
  }
"""
if text.count(old) != 1:
    raise SystemExit(f"tray update rebuild source changed upstream: found {text.count(old)}")
path.write_text(text.replace(old, new))
