# Indigo Stats for Unraid

This repository contains the Unraid Community Applications metadata for [Indigo Stats](https://github.com/dbulnes/indigo-stats), a private dashboard that polls a PurpleAir sensor on the local network and stores minute-level temperature, humidity, PM2.5, US AQI, and history.

The application source, Dockerfile, tests, and release workflow live only in the application repository. This repository contains only the Unraid template, repository profile, icon, and packaging documentation.

## Publication status

This package passed the Community Applications submission portal's Validate and Scan checks and was submitted for publication on September 20, 2026. The public `ghcr.io/dbulnes/indigo-stats:latest` image provides the supported `linux/amd64` runtime, and this repository is the canonical source for its Unraid metadata and support path.

The template is currently marked beta because the `0.1.x` application is still under active development. The label can be removed when the application is ready to be presented as stable.

## Installation

In Unraid, open **Apps**, search for **Indigo Stats**, review the configuration, and select **Install**. The canonical template is [`templates/indigo-stats.xml`](templates/indigo-stats.xml), and its public raw URL can also be used by tooling that supports external templates:

```text
https://raw.githubusercontent.com/dbulnes/indigo-stats-unraid/main/templates/indigo-stats.xml
```

The application exposes container port `8000`; the template maps host port `8765` by default. The WebUI entry uses `[PORT:8000]`, allowing Unraid to resolve a changed host-side port correctly.

## Configuration

| Setting | Default | Purpose |
| --- | --- | --- |
| Web UI port | `8765` | Trusted-LAN HTTP access to container port `8000` |
| Appdata | `/mnt/user/appdata/indigo-stats` | Persistent SQLite database and local snapshots mounted at `/data` |
| PurpleAir sensor IP | none; required | Private IPv4 address of the local sensor |
| Timezone | `Etc/UTC` | IANA timezone used in charts |
| PM2.5 method | `cf1` | Raw channel average or the EPA 2021 outdoor correction |
| Temperature and humidity | `purpleair` | PurpleAir estimated, raw operating, or simple adjusted display |
| Forecasts | disabled | Optional Open-Meteo weather and regional PM2.5 forecasts |
| Forecast coordinates | empty | Required as a pair when forecasts are enabled; masked in the template |
| PUID / PGID | `99` / `100` | Unraid user and group used after initialization |

The application has no login. Keep it on a trusted LAN or private tailnet and do not expose it directly to the internet. Configure HTTPS separately if mobile PWA installation is required. Forecast coordinates are sent to Open-Meteo only when forecasts are enabled. No street address is needed or exposed by this template.

## Persistence, upgrades, and removal

All mutable state is under `/data`. Container replacement or image updates preserve history when the same appdata mapping is retained. Never map the live SQLite database to SMB/NFS. Do not run two application containers against one data directory because both would start collectors.

Before upgrades, stop the container and make a consistent application backup with the current image. Keep the old image and backup until the new container has retained history and collected a new sample. Removing the container does not require removing appdata; deleting appdata permanently removes readings, settings, and local snapshots.

Local snapshots remain on the same storage and are not an off-server backup. See the [application operations guide](https://github.com/dbulnes/indigo-stats/blob/main/docs/operations.md) for backup and restore details.

## Container review notes

- Architectures: the published Unraid image is `linux/amd64`. The same Dockerfile builds `linux/arm64` locally for Apple Silicon testing, but that image is not published.
- Network: bridge mode; inbound TCP `8000`; local HTTP access to the configured sensor; optional outbound HTTPS to Open-Meteo.
- Storage: one read-write `/data` mount; root filesystem is read-only; `/tmp` is tmpfs.
- Privileges: privileged mode, host networking, Docker socket, host devices, and host service changes are not used.
- Capabilities: all are dropped, then `CHOWN`, `DAC_OVERRIDE`, `SETUID`, and `SETGID` are added solely so the entrypoint can initialize the dedicated appdata directory and drop to PUID/PGID.
- Secrets: there are no API credentials. Optional coordinates are masked because they are private location data.
- Shutdown: Uvicorn handles SIGTERM; the template allows a 35-second stop timeout.

## Updates and support

Application behavior and image problems belong in the [Indigo Stats application repository](https://github.com/dbulnes/indigo-stats/issues). Unraid template and Community Applications packaging problems belong in this repository's issue tracker.

The template repository is MIT licensed. The underlying Indigo Stats application remains under its own [Unlicense](https://github.com/dbulnes/indigo-stats/blob/main/LICENSE).

## Community Applications maintenance

Application-only releases are published from the application repository and do not require a template edit because the listing tracks `ghcr.io/dbulnes/indigo-stats:latest`. Before publishing one, verify the anonymous AMD64 pull, retained appdata, health, history, collection, backup integrity, and clean shutdown.

When installation metadata changes, update this repository's template, `Date`, and `Changes`; run `python3 scripts/validate.py`; push the change; and rerun the Community Applications portal's Validate and Scan checks. Keep every template and icon URL publicly accessible.
