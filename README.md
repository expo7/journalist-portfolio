# Candis Hart — Investigative Journalism Portfolio

A responsive, dependency-free portfolio for an investigative journalist. It presents selected reporting, a short professional profile, field-note links, a contact path for tips, and small interactive enhancements.

## Run locally

From the project directory, start a local static server:

```bash
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) in a browser. Stop the server with `Ctrl+C`.

## Main interactions

- Filter selected work by investigations or features.
- Open and close the mobile navigation.
- Submit the newsletter form to receive an in-page confirmation.
- Copy the public contact email from the footer.

The site is deliberately static: newsletter and contact endpoints are presentation-only and do not transmit or store personal data.

## Structure

- `index.html` — semantic site content and layout
- `styles.css` — responsive visual design and accessibility styles
- `script.js` — navigation, filtering, newsletter feedback, and copy-email behavior
