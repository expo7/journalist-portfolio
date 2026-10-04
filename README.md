# Kandace Baez — Investigative Journalism Portfolio

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

## Editorial content backup and import

`portfolio/fixtures/editorial_content.json` is a portable snapshot of the site profile, stories, and field notes. It deliberately excludes Django users and passwords, contact/tip messages, and uploaded files.

After running migrations on a new server, validate and then import the fixture:

```bash
.venv/bin/python manage.py import_portfolio_content --dry-run
.venv/bin/python manage.py import_portfolio_content
```

The importer is idempotent: it updates the single site profile and matches stories and field notes by slug, so it can be used after the standard seed migrations. To create a newer backup from a local database, export only the editorial models:

```bash
.venv/bin/python manage.py dumpdata portfolio.siteprofile portfolio.story portfolio.fieldnote --indent 2 --output portfolio/fixtures/editorial_content.json
```

If the profile or stories use uploaded images/documents, copy the local `media/` directory to the destination media storage separately. Never export or commit `ContactMessage` records, user accounts, passwords, `db.sqlite3`, or `.env` files.

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


### Website styles
In Django admin, open Site profile → Website style. Choose Original — Paper Trail or Harbor Editorial — Navy & Ivory, save, then refresh the public site. The selection applies to the homepage and article pages.

The public page also has a Style selector for instant demo comparisons. It remembers the choice for this browser tab; the admin selection remains the site-wide default. An illustrated cat is shown when no headshot is uploaded.

An Admin link is temporarily visible in the homepage navigation and article header for the demo. Authentication is still required.

Harbor Rose is a third style: warmer ivory, muted plum, and soft rose/brass accents. It is available in both the on-page selector and admin.

### Kandace feedback iteration

**Site profile** now groups editing into Appearance (style, headshot upload, custom logo or KB monogram), Optional sections (field notes and corkboard), Reader support, Publication credit, Identity, About, and Contact. Midnight Blue is a fourth style; prior options remain. Field notes default off. Reader support defaults off and requires a hosted payment URL as well as the switch; no payment account is created by this site.

**Stories** support topic tags and uploaded cover images; the publication date may be left blank until verified. **Corkboard items** are separate from field notes and default to unpublished. Only explicitly published items appear on the public board. Do not put confidential sources or private research in public summaries.

After migration, optionally run `python manage.py prepare_kandace_demo` to set Midnight as the default, reflect the supplied interests, add the supplied UFO article link without inventing a publication date, and link the publisher archive. This command retains unedited sample stories as unpublished drafts, preserves uploads and support settings, and does not overwrite an existing copy of the linked article. It updates the demo bio; review before running against edited production copy.

Pending editorial verification: full publisher article list and dates; whether “featured guest contributor” is her formal credit; the gorilla article/study and trip location; reference image for the precise navy color; her final logo and hosted donation URL. The gorilla topic is an interest, not a published scientific claim. Confirm these when Kandace supplies source material before adding detailed claims. No full publisher article text has been copied.

This is the reusable development pattern: preserve named style options, give optional sections independent switches, and keep content editing separate from appearance. A switch hides a section without deleting its records.

Latest direction: the corkboard was intended as a visual style, so the standalone research board and its admin entry are removed. Stored board records are retained for reversibility. Reader support defaults on with “Buy me a dog treat”; without a hosted payment URL it is clearly a disabled preview. Navigation and contact buttons use “Message” to distinguish correspondence from donations.

`python manage.py import_observer_links` adds the four distinct article links verified from the downloaded PDFs, including dates and installment subtitles. It corrects the original placeholder link and uses the byline-based credit “Special contributor.” It does not publish the downloaded PDFs or copy full article text.

Article cards open the publisher directly when no text or document is hosted locally; existing internal links redirect there too. The supplied nebula is the fallback card artwork. The on-page Hero image selector previews Lighthouse or Corkboard independently of the color style and remembers the selection for the tab. Admin → Site profile → Appearance sets the default hero image. Corkboard artwork is decorative, not a research section.

Correction: reader support says “Buy me cat treats.” The August 4 publisher PDF is the continuation of the July 28 driver’s-window article. Its heading and editor’s note use inconsistent numbering, so the portfolio labels it “continued” rather than asserting a new part number.

Midnight Glow adds the Deathmatch-style upper-right radial glow and diagonal panel gradients in the portfolio navy palette. The style menu retains every previous option. Contact inputs use white backgrounds and black text, and both Send message buttons share the same navy treatment in every style.

Logo options replace the KB monogram with three original SVG marks: Cat (curiosity), Lighthouse (clarity), and Pen & Star (independent voice). The on-page Logo dropdown remembers a tab preview; admin Appearance → Logo style sets the default. Uploaded logos remain available as a fourth preview choice.
