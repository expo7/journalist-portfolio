# Kandace Biaz — Investigative Journalism Portfolio

A responsive Django portfolio for an investigative journalist. The public site displays reporting and field notes from the database; Django's built-in, password-protected admin lets an editor publish, edit, hide, and reorder that content.

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

- **Stories:** title, publication, publish date, category, deck, optional article URL, visual treatment, feature state, visibility, and ordering.
- **Field notes:** title, publish date, optional destination URL, visibility, and ordering.

Only records marked **Published** appear publicly. `sort_order` controls display order (lower numbers appear first). The initial migration adds the three example stories and notes shown in the original design.

## Security and deployment

The local configuration runs with `DJANGO_DEBUG=1`. Before deployment, set `DJANGO_DEBUG=0`, a unique `DJANGO_SECRET_KEY`, and a comma-separated `DJANGO_ALLOWED_HOSTS`; Django refuses to start in non-debug mode without a secret key. Do not commit `.env`, database files, or admin passwords.

## Checks

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

## Project layout

- `config/` — Django project configuration and URLs
- `portfolio/models.py` — editable story and field-note models
- `portfolio/admin.py` — editorial admin interface
- `portfolio/templates/portfolio/home.html` — public portfolio template
- `portfolio/static/portfolio/` — stylesheet and browser interactions
