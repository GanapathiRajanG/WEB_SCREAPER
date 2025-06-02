# NeoScraper - Django Web Scraper

This project has been successfully converted from Flask to Django. NeoScraper is an advanced web content extractor that analyzes websites and extracts key information including headings, metadata, important content, images, and links.

## 🚀 Features

- **Web Scraping**: Extract content from any website
- **Modern UI**: Beautiful, animated interface with glassmorphism design
- **Content Analysis**: Extracts headings, bold text, paragraphs, images, and links
- **History Tracking**: Stores and displays previous scraping sessions
- **Django Admin**: Full admin interface for managing scraped data
- **REST API**: JSON endpoints for programmatic access

## 📁 Project Structure

```
web_scraper_django/
├── manage.py
├── requirements.txt
├── README.md
├── web_scraper_django/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── scraper/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── migrations/
    └── templates/
        └── scraper/
            └── index.html
```

## 🔄 Conversion Changes

### From Flask to Django:

1. **Database**: 
   - **Before**: MongoDB with PyMongo
   - **After**: SQLite with Django ORM and JSONField for complex data

2. **Models**: 
   - Created `ScrapedData` model with proper fields and relationships
   - Used JSONField to store complex content structures

3. **Views**: 
   - Converted Flask routes to Django function-based views
   - Maintained same API endpoints and functionality

4. **Templates**: 
   - Moved HTML template to Django template structure
   - No changes needed to the frontend code

5. **URL Routing**: 
   - Created Django URL patterns
   - Maintained same endpoint structure

## 🛠️ Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**:
   - Main App: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📡 API Endpoints

- `GET /` - Main application interface
- `POST /scrape/` - Scrape a website (JSON: `{"url": "https://example.com"}`)
- `GET /history/` - Get scraping history

## 🎯 Usage

1. Open the web interface at http://127.0.0.1:8000/
2. Enter a website URL in the input field
3. Click "Analyze" to scrape the website
4. View extracted content organized by type
5. Check the history section for previous scrapes

## 🔧 Technical Details

- **Framework**: Django 4.2.7
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Frontend**: Vanilla JavaScript with modern CSS animations
- **Scraping**: BeautifulSoup4 + Requests
- **Storage**: Django ORM with JSONField for complex data structures

## 🎨 Features Maintained

All original Flask functionality has been preserved:
- ✅ Website content extraction
- ✅ Metadata parsing
- ✅ Content categorization
- ✅ History tracking
- ✅ Modern UI/UX
- ✅ Error handling
- ✅ Responsive design

## 🆕 New Django Features

- **Admin Interface**: Full CRUD operations on scraped data
- **ORM Benefits**: Better data relationships and queries
- **Scalability**: Django's robust architecture for future expansion
- **Security**: Django's built-in security features
- **Testing**: Django's comprehensive testing framework ready to use

## 🚀 Next Steps

The Django conversion is complete and fully functional. You can now:
- Add user authentication
- Implement more advanced scraping features
- Add data export functionality
- Scale with Django's ecosystem
- Deploy using Django deployment best practices
