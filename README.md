# Kandace Biaz — Investigative Journalism Portfolio

A responsive Django portfolio for an investigative journalist. The public site displays reporting and field notes from the database; Django's built-in, password-protected admin lets an editor manage site content and received messages.

## Local setup

The commands below create an isolated environment, install the application dependency, initialize the local database with the sample portfolio, and start the site:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the public portfolio.

## Admin account and content editing

Create the editor account locally (choose a strong password when prompted):

```bash
.venv/bin/python manage.py createsuperuser
```

Sign in at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). The admin provides:

- **Stories:** title, publication, publish date, category, deck, visual treatment, feature state, visibility, and ordering. Paste full text into **Article body** to host and display it on the site; upload a PDF, Word document, or text file for visitors to download; optionally retain an **External publication** URL.
- **Field notes:** title, publish date, optional destination URL, visibility, and ordering.
- **Site profile:** editable name, hero copy, bio, beat/location details, public email addresses, footer copy, and an optional headshot upload.
- **Contact messages:** a private inbox of contact requests and anonymous tips submitted through the public site. Mark entries read once handled.

Only records marked **Published** appear publicly. `sort_order` controls display order (lower numbers appear first). The initial migration adds the three example stories and notes shown in the original design.

### Publishing an article on the site

Create or edit a **Story** in the admin. The story card always opens a public reading page at `/reporting/<slug>/`.

- Paste the article into **Article body** to show it directly on that page. Paragraph breaks are preserved.
- Upload a PDF, `.doc`, `.docx`, or `.txt` file to **Article file** to offer it as a download.
- Add an **External publication** URL to keep a link to the original publisher. It appears alongside the hosted article or download.

## Contact and tips

The public **Contact** section posts directly to the Django application and stores each submission in the private **Contact messages** admin inbox. Standard contact requests require a name, email address, and message. Tips can be anonymous; the form intentionally warns visitors not to upload or transmit sensitive documents through the website.

The form includes CSRF protection and a hidden honeypot field to reject basic automated submissions. It does not send email or expose message content publicly. Configure email delivery separately if notification emails are needed.

## Security and deployment

The local configuration runs with `DJANGO_DEBUG=1`. Before deployment, set `DJANGO_DEBUG=0`, a unique `DJANGO_SECRET_KEY`, and a comma-separated `DJANGO_ALLOWED_HOSTS`; Django refuses to start in non-debug mode without a secret key. Uploaded headshots are saved under `media/`, which is deliberately ignored by Git. Configure secure media storage and HTTPS before a production deployment. Do not commit `.env`, database files, uploads, or admin passwords.

## Checks

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

## Handoff notes

- The public site is database-driven; run `migrate` before starting it so the seeded profile, stories, and notes are available.
- `db.sqlite3`, `media/`, `.env`, and `.venv/` are local-only and intentionally ignored. Create a new admin account locally with `createsuperuser`; no account credentials are stored in Git.
- Existing migrations are additive and must remain in version control. Create a new migration whenever a model changes.
- The public pages are `home` and `story_detail`; editorial content and incoming messages are administered through Django admin.

## Project layout

- `config/` — Django project configuration and URLs
- `portfolio/models.py` — editable stories, field notes, site profile, and contact-message models
- `portfolio/admin.py` — editorial CMS and private message-inbox interface
- `portfolio/forms.py` and `portfolio/views.py` — public contact/tip submission and page behavior
- `portfolio/templates/portfolio/home.html` — public portfolio template
- `portfolio/templates/portfolio/story_detail.html` — hosted article reader
- `portfolio/static/portfolio/` — stylesheet and browser interactions
