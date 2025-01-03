# Backend - In All Fonts

A brief description of the project and its purpose.

## Table of Contents

- [Backend - In All Fonts](#backend---in-all-fonts)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Development Workflow](#development-workflow)

---

## Prerequisites

- **Python 3.7+** (Python 3.13 is recommended, but anything 3.7+ should generally work with Django 5)
- **Virtual Environment** (recommended)
- **Git** (to clone the repository)

_(On some systems, you may need libraries for Pillow, e.g., libjpeg. Most modern OS distributions already include them.)_

---

## Installation

1. **Clone this repository**:

   ```bash
   git clone https://github.com/gabeha/inallfonts-backend.git
   cd inallfonts-backend
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv env
   source env/bin/activate
   ```

   - On Windows:
     ```powershell
     python -m venv env
     .\env\Scripts\activate
     ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run initial migrations** to set up the database:

   ```bash
   python manage.py migrate
   ```

5. **(Optional) Create a superuser** for the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

7. **Navigate to** `http://127.0.0.1:8000/` in your browser.
   - For the DRF-based API, you can find the browsable API at `http://127.0.0.1:8000/api/`.

---

## Usage

- **Uploading Images**: Since we’re using `pillow` for image handling, you can upload images to certain endpoints (like `/api/challenges/`). Ensure you have `MEDIA_ROOT` and `MEDIA_URL` configured in `settings.py`.

- **Admin Site**: If you created a superuser, you can log into the Django Admin at `http://127.0.0.1:8000/admin/`.

---

## Development Workflow

1. **Make changes** in your code (models, views, etc.).
2. **Run migrations** whenever you change models:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Run tests** (if applicable):

   ```bash
   python manage.py test
   ```

4. **Commit and push** to GitHub.
