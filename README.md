[![Validate Unraid metadata](https://github.com/dbulnes/indigo-stats-unraid/actions/workflows/validate.yml/badge.svg)](https://github.com/dbulnes/indigo-stats-unraid/actions/workflows/validate.yml)
# Indigo: Local PurpleAir Stats for Unraid

<p align="center">
  <img src="https://raw.githubusercontent.com/dbulnes/indigo-stats-unraid/main/docs/screenshot_overview.png" alt="Indigo Stats Overview Dashboard" width="800"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dbulnes/indigo-stats-unraid/main/docs/screenshot_history.png" alt="Indigo Stats History & Telemetry" width="800"/>
</p>

Indigo Stats is a private air-quality and weather dashboard for a PurpleAir sensor on your local network. It collects readings every minute, keeps long-term history on your Unraid server, and presents current conditions and trends in a responsive web app that can be installed as a PWA.

This repository provides the Unraid Community Applications package. The [Indigo Stats application repository](https://github.com/dbulnes/indigo-stats) contains the source code and detailed technical documentation.

## Features

- Collects temperature, humidity, both PM2.5 channels, quality flags, and corrected PM2.5 directly from a PurpleAir sensor on the LAN.
- Calculates US AQI estimates with EPA 2024 breakpoints and displays PM2.5 NowCast after enough complete hourly history is available.
- Makes historical exploration easy with date ranges, time navigation, previous-period overlays, threshold inspection, daily patterns, and CSV export.
- Optionally compares local readings with hourly regional weather and PM2.5 forecasts from Open-Meteo.
- Shows collector, forecast, database, backup, and storage health.
- Stores state in SQLite under persistent Unraid appdata and creates consistent daily snapshots.
- Provides an installable React/TypeScript PWA from the same container.

## Requirements

- An AMD64 Unraid server.
- A PurpleAir sensor reachable from the container over the same private network.
- A dedicated local appdata directory for the SQLite database and backups.
- Optional outbound HTTPS access and coordinates if regional forecasts are enabled.

Indigo Stats has no application login. Keep it on a trusted LAN or private tailnet and do not expose it directly to the internet. PWA installation on mobile devices normally requires HTTPS through a private reverse proxy or Tailscale Serve configured separately.

## Installation

1. Open the **Apps** tab in Unraid and search for **Indigo Stats**.
2. Select **Install**.
3. Enter the PurpleAir sensor's private IPv4 address and your IANA timezone.
4. Review the PM2.5 and temperature/humidity display methods.
5. To enable forecasts, turn them on and provide both latitude and longitude. Otherwise, leave forecasts disabled and both coordinates empty.
6. Apply the template, wait for the container to become healthy, and open **WebUI**.

The template maps container port `8000` to host port `8765` by default. You may choose another available host port. The [container template](https://github.com/dbulnes/indigo-stats-unraid/blob/main/templates/indigo-stats.xml) tracks the latest published AMD64 image at `ghcr.io/dbulnes/indigo-stats:latest`.

## Configuration

| Setting | Default | Purpose |
| --- | --- | --- |
| Web UI port | `8765` | Trusted-network HTTP access to the dashboard |
| Appdata | `/mnt/user/appdata/indigo-stats` | Persistent database, settings, and local snapshots mounted at `/data` |
| PurpleAir sensor IP | Required | Private IPv4 address of the local sensor |
| Timezone | `Etc/UTC` | IANA timezone used in charts |
| PM2.5 method | `cf1` | Raw channel average or EPA 2021 outdoor correction |
| Temperature and humidity | `purpleair` | PurpleAir estimated, raw operating, or simple adjusted display |
| Regional forecasts | Disabled | Optional Open-Meteo weather and PM2.5 forecasts |
| Forecast coordinates | Empty | Required as a pair when forecasts are enabled |
| PUID / PGID | `99` / `100` | Unraid user and group used by the application |

No street address or API credential is required. Forecast coordinates are sent to Open-Meteo only when forecasts are enabled and are not returned by dashboard APIs.

## History, persistence, and backups

All mutable state is stored under `/data`. Unraid container updates preserve readings and settings as long as the same appdata path remains mapped to `/data`. Removing the container does not remove appdata unless you explicitly delete that directory.

Minute-level readings are retained indefinitely by default. Raw sensor payloads expire after 30 days. The application creates daily SQLite snapshots and retains the latest 14 on the same appdata volume. These snapshots help with some application or operator mistakes, but they do not protect against loss of the Unraid server or its storage.

Use local SSD-backed appdata for the live SQLite database. Do not place it on SMB or NFS, and do not run two Indigo Stats containers against the same data directory.

## Updates and data safety

Apply normal image updates from Unraid's Docker or Apps interface. An update replaces the container image while retaining the `/data` mapping; it must not delete or replace the existing appdata directory.

Before an update, keep a consistent backup and the previous image until you confirm that the new container shows the existing history and collects a new sample. See the [operations guide](https://github.com/dbulnes/indigo-stats/blob/main/docs/operations.md) for backup, upgrade, restore, HTTPS, and troubleshooting details.

## Support and source

- For dashboard behavior, collection, forecasts, database, or image problems, use the [Indigo Stats issue tracker](https://github.com/dbulnes/indigo-stats/issues).
- For Unraid installation or template problems, use the [Unraid package issue tracker](https://github.com/dbulnes/indigo-stats-unraid/issues).
- Application source and releases: [dbulnes/indigo-stats](https://github.com/dbulnes/indigo-stats)
- Published container image: [GitHub Container Registry](https://github.com/dbulnes/indigo-stats/pkgs/container/indigo-stats)

The Unraid package metadata is MIT licensed. The Indigo Stats application uses the [Unlicense](https://github.com/dbulnes/indigo-stats/blob/main/LICENSE).
