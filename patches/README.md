# Noctalia V5 source patches

Each script patches one compatibility concern and aborts when its expected upstream source no longer matches. `noctalia-v5.nix` applies them in the order listed below. These anchors target Noctalia 5.4.0.

1. `patch-media-mini.py` — add the APIs required by the optional V4 MediaMini plugin; the native `media` widget remains available.
2. `patch-stable-output.py` — stable make/model/serial identities for desktop-widget outputs.
3. `patch-screenshot-secondary-click.py` — add `widget.*.secondary_click = "menu" | "fullscreen"` (native default: `menu`).
4. `patch-panel-prewarm-blur.py` — disable panel blur prewarming.
5. `patch-icon-raster-quality.py` — improve launcher, workspace/taskbar, and tray HiDPI icon rasterization.
6. `patch-tray-drawer-relayout.py` — lay drawer icons out again after the async icon-theme scan rebuilds them.
7. `patch-panel-click-anchor.py` — anchor attached panels to the widget that opened them.
8. `patch-panel-background-opacity.py` — keep panel opacity independent of transparent bar opacity.
9. `patch-panel-compositor-blur.py` — add `shell.panel.compositor_blur_enabled` (native default: `true`).
10. `patch-icon-theme-environment.py` — add `theme.icon_theme_source = "system" | "qs_environment"` (native default: `system`).
11. `patch-notification-timeouts.py` — add native/application and urgency-specific notification timeout policies (native default: application timeout).
12. `patch-deskvis-renderer.py` — add a per-instance `visualizer_profile = "native" | "v4"` renderer choice (native default: `native`).
13. `patch-deskvis-smoothing.py` — select V4 attack/decay only for desktop visualizers using the V4 profile.
14. `patch-deskvis-idle-fade.py` — select the 600 ms fade only for desktop visualizers using the V4 profile.
15. `patch-spectrum-frequency-range.py` — add configurable shared spectrum cutoffs (native defaults: 20–20000 Hz).
16. `patch-taskbar-title-color.py` — make flat taskbar window titles honor the widget foreground color (native fallback remains `on_surface`).
17. `patch-control-center-eight-shortcuts.py` — allow up to 8 Control Center Home shortcuts in the grid and Settings (native default shortcuts remain unchanged).

Bar blur and OSD hide delay are native in 5.4.0. Transparent bars set `compositor_blur = false`, and `osd.hide_delay_ms` stays in `config.toml`. Whole-widget hover highlight is disabled with `hover_highlight = false`.
