# Kerala-Style Blog Website

A Django-based blogging platform featuring traditional Kerala-style Malayalam blogs with modern features including text-to-speech capabilities.

## Features

- User authentication and authorization
- Blog post creation and management
- Comments system
- Blogger profiles
- Text-to-Speech functionality
- Responsive design
- Admin panel

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to view the site.
