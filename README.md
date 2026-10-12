# SkillSwap

A small Django project with signup, username/password login, POST logout, and a protected account page.

## Run locally (PowerShell)

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/signup/ to create an account.

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py test
```

## Simple structure

- `accounts/models.py`: `User(AbstractUser)` with full name, unique email, bio, location, and optional profile picture. Django supplies the ID, username, hashed password, first/last names, permissions, and date joined.
- `accounts/forms.py`: signup using Django's `UserCreationForm` and password validation.
- `accounts/views.py`: signup with automatic login, and a protected home page.
- `accounts/urls.py`: Django's built-in login and logout views.
- `templates/`: shared layout and authentication pages.
- `static/css/style.css`: responsive light theme and reusable palette variables.

Profile fields are stored on the user; profile editing and image uploads are outside this authentication setup. Ratings can be calculated from reviews when those models are added. Skills belong in separate Skill/UserSkill models.

This is a local development configuration. Before deployment, set a private `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, and configure your deployment hosts and HTTPS.

## Light color palette

| Role | Color | CSS variable |
| --- | --- | --- |
| Page background | `#F5F8F7` | `--background` |
| Cards and inputs | `#FFFFFF` | `--surface` |
| Primary / links | `#187D5B` | `--primary` |
| Primary hover | `#126347` | `--primary-hover` |
| Soft green accent | `#E8F5EE` | `--accent` |
| Main text | `#182B24` | `--text` |
| Secondary text | `#56675F` | `--muted` |
| Borders | `#D5DFD9` | `--border` |
| Errors | `#B42318` | `--error` |
