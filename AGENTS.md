# Indigo Stats Unraid packaging instructions

These instructions apply to the entire repository.

## Repository purpose and boundaries

This repository owns only the Unraid Community Applications package for Indigo Stats: the container template, CA profile, icon, public package README, validation script, and packaging workflow.

Application source, Dockerfile, tests, runtime documentation, database migrations, and image publishing belong in [dbulnes/indigo-stats](https://github.com/dbulnes/indigo-stats). Do not duplicate them here. Update this repository only when installation metadata, configuration fields, defaults, ports, paths, security options, support links, category, icon, or other CA-facing information changes.

## Public README

`README.md` is displayed to prospective users through GitHub and the template's `<ReadMe>` URL. Keep it focused on what Indigo Stats does, requirements, installation, configuration, persistence, updates, privacy, and support.

Do not put submission checklists, portal instructions, review status, release mechanics, agent instructions, or temporary draft language in the README. Keep maintainer procedures in this file. Do not hard-code the current application version in the README because the template follows the stable `latest` image tag.

## Privacy and host safety

- Never commit a real address, coordinates, sensor IP, homelab IP or hostname, tailnet URL, credentials, database, backup, or raw sensor payload.
- Leave `SENSOR_HOST`, `FORECAST_LATITUDE`, and `FORECAST_LONGITUDE` empty in the public template. Coordinate fields must remain masked.
- Never deploy to, inspect, scan, or remove anything from an Unraid host unless the user explicitly requests that host action in the current task.
- Preserve the `/data` appdata mapping. Container updates must never delete, replace, or initialize over existing user data.
- Do not add privileged mode, host networking, Docker socket access, host devices, SSH, automatic Tailscale changes, or host service changes.

## Template invariants

- Keep the image at `ghcr.io/dbulnes/indigo-stats:latest`; the application repository publishes stable AMD64 releases with GitHub Actions and `GITHUB_TOKEN`.
- The supported Unraid runtime is `linux/amd64`. ARM64 images are for local development in the application repository and are not published.
- Keep bridge networking, container port `8000`, persistent `/data`, the read-only root filesystem, `/tmp` tmpfs, dropped capabilities, the minimal documented capability additions, `no-new-privileges`, and the graceful stop timeout unless an application change requires an audited update.
- Keep `<Support>` pointed to this repository's issues and `<Project>` pointed to the application repository.
- Keep `<ReadMe>`, `<Icon>`, and `<TemplateURL>` publicly accessible through raw GitHub URLs.
- Retain `<Beta>true</Beta>` while the application is under active development. Remove it only when the user explicitly declares the application stable.

## Validation and Community Applications maintenance

Run before every commit:

```sh
python3 scripts/validate.py
```

The validator checks XML structure, required fields, public defaults, masked location fields, README audience, and known private deployment identifiers.

When the template changes, update `<Date>` and `<Changes>` with concise user-facing information. Confirm that the icon, template, README, project, registry, and support URLs resolve publicly. Push the reviewed commit, wait for repository CI to pass, and rerun Community Applications Validate and Scan when the portal requires it.

Application-only releases need no packaging commit because the template tracks `latest`. Before changing the template for an application release, confirm that its ports, paths, variables, defaults, architecture, and security requirements actually changed.

The package passed the submission portal's Validate and Scan checks and was submitted on September 20, 2026. Do not describe it as an unpublished draft or repeat the initial submission checklist in public documentation.

## Working practices

Make small, coherent commits and push `main` after validation. Keep packaging changes separate from application changes. Do not add Docker Hub credentials, registry secrets, or duplicated image publishing workflows to this repository.
