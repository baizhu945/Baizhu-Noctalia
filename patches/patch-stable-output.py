#!/usr/bin/env python3
"""Give desktop widgets stable make/model/serial output identities."""

from pathlib import Path


def replace(path: str, old: str, new: str, label: str) -> None:
    target = Path(path)
    text = target.read_text()
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match in {path}, found {count}")
    target.write_text(text.replace(old, new))


replace(
    "src/shell/desktop/desktop_widget_layout.h",
    """  inline std::string outputKey(const WaylandOutput& output) {
    if (!output.connectorName.empty()) {
      return output.connectorName;
    }
    return std::to_string(output.name);
  }

  inline const WaylandOutput* findOutputByKey(const WaylandConnection& wayland, const std::string& key) {
""",
    """  // Connector names such as eDP-1/eDP-2 are allocation-order dependent.
  // Prefer a hardware identity from wlr-output-management and include a real
  // serial when the monitor exposes one. The connector remains a legacy alias
  // in findOutputByKey(), so old settings migrate without disappearing.
  inline std::string outputKey(const WaylandOutput& output) {
    if (!output.model.empty()) {
      std::string key = "hardware:";
      key += output.make.empty() ? "*" : output.make;
      key += '|';
      key += output.model;
      if (!output.serialNumber.empty() && output.serialNumber != "Unknown") {
        key += '|';
        key += output.serialNumber;
      }
      return key;
    }
    if (!output.connectorName.empty()) {
      return output.connectorName;
    }
    return std::to_string(output.name);
  }

  inline const WaylandOutput* findOutputByKey(const WaylandConnection& wayland, const std::string& key) {
""",
    "stable desktop output key",
)

replace(
    "src/shell/desktop/desktop_widget_layout.h",
    """      if (outputKey(output) == key) {
        return &output;
      }
""",
    """      if (outputKey(output) == key || output.connectorName == key || output.description == key) {
        return &output;
      }
""",
    "stable and legacy desktop output lookup",
)
replace(
    "src/shell/desktop/desktop_widget_layout.h",
    """          && (selector.empty() || outputKey(output) == selector)) {
""",
    """          && (selector.empty() || outputKey(output) == selector || output.connectorName == selector)) {
""",
    "exact connector selection",
)
replace(
    "src/shell/lockscreen/lockscreen_login_box.cpp",
    """      if (selection.output != nullptr && desktop_widgets::outputKey(*selection.output) == outputKey) {
""",
    """      if (selection.output != nullptr
          && (desktop_widgets::outputKey(*selection.output) == outputKey
              || selection.output->connectorName == outputKey)) {
""",
    "login box connector alias",
)
replace(
    "tests/desktop_widget_output_test.cpp",
    """    TEST_CHECK(generated->outputName == "DP-11");
""",
    """    TEST_CHECK(generated->outputName == "hardware:Acme|Landscape|LANDSCAPE123");
""",
    "login box hardware identity",
)
