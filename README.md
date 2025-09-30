# TechPulse (Django + SQLite)

## Prereqs
- Python 3.11+
- (Optional) Nginx + systemd for production

## Quick start (dev)
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/sources.json
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/admin and http://127.0.0.1:8000/api/news/articles

## Fetch news
Run manually:
```bash
python manage.py fetch_news
```

Or every 15 minutes with cron/systemd timer (see deploy/).

## API examples
- `GET /api/news/articles?search=AI&ordering=published_at`
- `GET /api/news/sources`
- `GET /api/comments/`
- `POST /api/comments/` with JSON `{ "article": <id>, "body": "Nice read!" }` (session-auth)

## Production (Ubuntu) — Nginx + Gunicorn + systemd
1) Install packages:
```bash
sudo apt update && sudo apt install -y python3-venv nginx
```

2) Create service user and layout (example):
```bash
sudo adduser --system --group --home /srv/techpulse techpulse
sudo rsync -a ./ /srv/techpulse/app/
sudo -u techpulse bash -lc 'python3 -m venv /srv/techpulse/venv && /srv/techpulse/venv/bin/pip install -r /srv/techpulse/app/requirements.txt'
sudo -u techpulse bash -lc 'cd /srv/techpulse/app && python manage.py migrate && python manage.py collectstatic --noinput'
```

3) systemd services:
- Copy files from `deploy/systemd/` and enable:
```bash
sudo cp deploy/systemd/techpulse.service /etc/systemd/system/
sudo cp deploy/systemd/techpulse-fetch.service /etc/systemd/system/
sudo cp deploy/systemd/techpulse-fetch.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now techpulse.service techpulse-fetch.timer
```

4) Nginx site:
```bash
sudo cp deploy/nginx/techpulse /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/techpulse /etc/nginx/sites-enabled/techpulse
sudo nginx -t && sudo systemctl reload nginx
```

## Azure (later)
- Swap SQLite → Azure Database for PostgreSQL
- Host on Azure App Service or VM Scale Set behind Azure Load Balancer
- Static files on Azure Blob Storage
- Scheduler via WebJobs or Functions timer
