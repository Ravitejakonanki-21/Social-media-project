# Django Social Media Platform (Major Project)

A production-grade Django social media platform with authentication, posts, comments, likes, friends, follow system, notifications, real-time WebSockets, and REST API.

## Features

| Feature | Status |
|--------|--------|
| Authentication (register / login / logout) | ✅ |
| User profiles (bio, picture, cover, location) | ✅ |
| Posts & comments | ✅ |
| Likes | ✅ |
| Friends & follow system | ✅ |
| Notifications (like, comment, friend request, follow) | ✅ |
| Real-time (Channels WebSocket) | ✅ |
| REST API (DRF) | ✅ |
| Search (posts) | ✅ |
| Privacy (public / friends visibility) | ✅ |
| Deployment-ready (Whitenoise, env vars, PostgreSQL) | ✅ |

## Prerequisites

- Python 3.10+
- Git
- PostgreSQL (optional; SQLite used by default for development)
- Virtual environment recommended

## Setup

### 1. Clone and enter project

```bash
cd task-2
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables (optional)

Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

For production set `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, and optionally `DATABASE_URL`, `REDIS_URL`.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

- **Web app:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **API root:** http://127.0.0.1:8000/api/

## Project structure

```
social_platform/
├── social_platform/     # Project settings, urls, asgi
├── users/              # Auth, profiles, signals
├── posts/              # Posts, comments, likes, feed, search
├── friends/            # Friend requests, follow
├── notifications/      # Notifications, WebSocket consumer
├── api/                 # DRF serializers, viewsets
├── templates/           # Bootstrap templates
├── media/               # User uploads (created at runtime)
├── static/              # Optional static files
├── manage.py
├── requirements.txt
└── README.md
```

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/posts/` | List / create posts |
| GET/PUT/PATCH/DELETE | `/api/posts/{id}/` | Retrieve / update / delete post |
| POST | `/api/posts/{id}/like/` | Toggle like |
| GET/POST | `/api/comments/` | List / create comments |
| GET | `/api/profiles/` | List profiles (search: username, bio, location) |
| GET/POST | `/api/friend-requests/` | List / send friend requests |
| POST | `/api/friend-requests/{id}/accept/` | Accept request |
| GET/POST | `/api/follows/` | List / create follow |
| GET | `/api/notifications/` | List notifications (authenticated) |
| POST | `/api/notifications/{id}/mark_read/` | Mark as read |

Filtering and search:

- Posts: `?author=1`, `?visibility=public`, `?search=keyword`
- Comments: `?post=1`, `?author=1`
- Follows: `?follower=1`, `?following=2`

## Web app pages

- **Feed:** `/` — posts, search, create post, like, comment
- **Profile:** `/users/profile/<username>/` — profile and posts
- **Edit profile:** `/users/profile/edit/`
- **New post:** `/posts/create/`
- **Friends:** `/friends/` — requests and friends list
- **Notifications:** `/notifications/`

## Deployment checklist

- Set `DEBUG=False`
- Set strong `SECRET_KEY` and `ALLOWED_HOSTS`
- Use PostgreSQL: set `DATABASE_URL` (e.g. `dj-database-url` on Railway/Render)
- Use Redis for Channels: set `REDIS_URL`
- Static files: Whitenoise is configured; run `python manage.py collectstatic`
- Media: configure cloud storage (e.g. S3) or use platform’s persistent storage

## Testing

```bash
python manage.py test
```

## Screenshots
<img width="1920" height="952" alt="Screenshot 2026-01-30 at 10 48 24 AM" src="https://github.com/user-attachments/assets/b09dfdeb-3c54-4cae-a9e7-4e07cef05be7" />
<img width="1919" height="955" alt="Screenshot 2026-01-30 at 10 49 12 AM" src="https://github.com/user-attachments/assets/4b6f6aff-774c-45ff-bbe5-a05302825dc6" />



## License

MIT (or as required by your institution).
