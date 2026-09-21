from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).parents[1]
profile = ET.parse(root / "ca_profile.xml").getroot()
assert profile.tag == "CommunityApplications"
assert (profile.findtext("Profile") or "").strip()

template = ET.parse(root / "templates" / "indigo-stats.xml").getroot()
assert template.tag == "Container" and template.attrib.get("version") == "2"
required = ("Name", "Repository", "Registry", "Network", "Privileged", "Support", "Project", "Overview", "WebUI", "Icon", "TemplateURL")
for tag in required:
    assert (template.findtext(tag) or "").strip(), f"missing {tag}"
assert template.findtext("Repository") == "ghcr.io/dbulnes/indigo-stats:latest"
assert template.findtext("WebUI") == "http://[IP]:[PORT:8000]/"
assert template.findtext("Privileged") == "false"

readme = (root / "README.md").read_text()
for maintainer_only_phrase in (
    "pre-release draft",
    "Do not submit it to Community Applications",
    "Before a Community Applications listing exists",
    "submission portal",
    "Validate and Scan",
    "Community Applications maintenance",
):
    assert maintainer_only_phrase not in readme, f"maintainer-only README text: {maintainer_only_phrase}"
for heading in (
    "## Features",
    "## Installation",
    "## Configuration",
    "## Updates and data safety",
    "## Support and source",
):
    assert heading in readme, f"missing public README section: {heading}"

fields = {item.attrib["Target"]: item for item in template.findall("Config")}
for target in ("8000", "/data", "SENSOR_HOST", "TZ", "PM_METHOD", "ENVIRONMENT_MODE", "FORECAST_ENABLED", "FORECAST_LATITUDE", "FORECAST_LONGITUDE", "PUID", "PGID"):
    assert target in fields, f"missing Config for {target}"
for target in ("SENSOR_HOST", "FORECAST_LATITUDE", "FORECAST_LONGITUDE"):
    assert not (fields[target].text or "").strip(), f"private default set for {target}"
for target in ("FORECAST_LATITUDE", "FORECAST_LONGITUDE"):
    assert fields[target].attrib.get("Mask") == "true"

forbidden_values = tuple(bytes.fromhex(value) for value in (
    "3138353135",
    "31302e31302e31302e3238",
    "31302e31302e31302e313030",
    "706561666f776c2d6d6f6f6e657965",
    "636e787169757977697162646668647a666d626e",
))
for path in root.rglob("*"):
    if path.is_file() and ".git" not in path.parts:
        data = path.read_bytes()
        for forbidden in forbidden_values:
            assert forbidden not in data, f"private deployment identifier in {path.relative_to(root)}"

print("Unraid metadata validation passed")
