# Alumni Management & Networking System (Flask + MySQL + Static Frontend)

Folders:
- backend: Flask API (models, controllers, routes)
- frontend: static HTML/CSS/JS pages under /pages

Quick start:
1. Install XAMPP and start Apache + MySQL.
2. Import mysql_schema.sql into phpMyAdmin or run it via CLI.
3. In backend/.env set DB credentials and JWT secret.
4. Create virtualenv, install requirements: pip install -r requirements.txt
5. Run backend: python app.py (runs at http://localhost:5000)
6. Serve frontend pages: cd frontend/pages; python -m http.server 8000
7. Open frontend: http://localhost:8000/index.html

Notes:
- Passwords are hashed with bcrypt.
- JWT is used for protected endpoints.
- Expand controllers/routes to add more endpoints and validation.
