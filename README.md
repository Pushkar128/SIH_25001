# SIH_25001
# CleanWater Hackathon Project

A static, role-based web app for reporting and viewing waterborne illness information.

## Project Structure

- `index.html` — Landing page linking to role portals
- `Homepage1.html` — Full marketing/home page with login modal
- `asha.html`, `doctor.html`, `citizen.html`, `official.html` — Role pages
- `assets/styles.css` — Shared styles (optional, existing role pages also include inline styles)
- `assets/app.js` — Small helper script (year + modal helpers)

## Run locally (Windows)

Option 1: Open directly (no server)
- Double-click `index.html` to open in your default browser.

Option 2: Simple Python server
- In PowerShell, run:
  ```powershell
  cd "C:\Users\rithe\Downloads\Codes\Hackathon"
  python -m http.server 8000
  ```
- Open `http://localhost:8000/index.html`

Option 3: Node http-server (if Node.js is installed)
- In PowerShell, run:
  ```powershell
  cd "C:\Users\rithe\Downloads\Codes\Hackathon"
  npx --yes http-server -p 8000 -c-1
  ```
- Open `http://localhost:8000/index.html`

## Notes
- The existing pages contain inline styles for portability. The new `assets` are used primarily by `index.html`.
- The login modal on `Homepage1.html` routes to role pages without authentication (demo only).
CleanWater is a comprehensive Smart Health Surveillance System designed to tackle the critical issue of waterborne diseases in communities. It provides a role-based platform for ASHA workers, doctors, citizens, and health officials to collaboratively monitor water quality and public health. This project was built by our team only for SIH Internal.
