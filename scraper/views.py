from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from bs4 import BeautifulSoup
import requests
import json
import re
from .models import ScrapedData


def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def scrape_website(url):
    """Scrape website and extract content - same logic as Flask version"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        metadata = {
            "title": clean_text(soup.title.string) if soup.title else "",
            "description": clean_text(soup.find("meta", attrs={"name": "description"})["content"]) if soup.find("meta", attrs={"name": "description"}) else "",
            "keywords": clean_text(soup.find("meta", attrs={"name": "keywords"})["content"]) if soup.find("meta", attrs={"name": "keywords"}) else "",
            "url": url,
            "scraped_at": timezone.now()
        }

        # Extract important content
        content = {
            "headings": [],
            "bold_texts": [],
            "important_paragraphs": [],
            "images": [],
            "links": []
        }

        # Headings (h1-h6)
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                text = clean_text(heading.get_text())
                if text:
                    content["headings"].append({
                        "text": text,
                        "level": i
                    })

        # Bold/strong/em text
        for tag in ['b', 'strong', 'em']:
            for element in soup.find_all(tag):
                text = clean_text(element.get_text())
                if text and text not in content["bold_texts"]:
                    content["bold_texts"].append(text)

        # Paragraphs with substantial content
        paragraphs = [clean_text(p.get_text()) for p in soup.find_all('p')]
        content["important_paragraphs"] = [p for p in paragraphs if len(p.split()) > 20][:10]

        # Images with alt text
        for img in soup.find_all('img', src=True):
            if img.get('alt', '').strip():
                content["images"].append({
                    "src": img['src'],
                    "alt": clean_text(img['alt'])
                })

        # Important links
        for link in soup.find_all('a', href=True):
            if len(clean_text(link.get_text())) > 3:
                content["links"].append({
                    "text": clean_text(link.get_text()),
                    "href": link['href']
                })

        # Save to database
        ScrapedData.objects.create(
            title=metadata["title"],
            description=metadata["description"],
            keywords=metadata["keywords"],
            url=metadata["url"],
            scraped_at=metadata["scraped_at"],
            headings=content["headings"],
            bold_texts=content["bold_texts"],
            important_paragraphs=content["important_paragraphs"],
            images=content["images"],
            links=content["links"]
        )

        return {
            "success": True,
            "metadata": metadata,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def index(request):
    """Home page view - equivalent to Flask's index route"""
    # Get recent scrapes from DB
    recent_scrapes = ScrapedData.objects.all()[:5]
    return render(request, 'scraper/index.html', {'recent_scrapes': recent_scrapes})


@csrf_exempt
@require_http_methods(["POST"])
def scrape_view(request):
    """Scrape endpoint - equivalent to Flask's /scrape route"""
    try:
        data = json.loads(request.body)
        url = data.get('url')

        if not url:
            return JsonResponse({"success": False, "error": "URL is required"}, status=400)

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        result = scrape_website(url)
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def get_history(request):
    """History endpoint - equivalent to Flask's /history route"""
    try:
        scrapes = ScrapedData.objects.all()[:20]

        # Convert to list of dictionaries for JSON serialization
        scrapes_data = []
        for scrape in scrapes:
            metadata = scrape.get_metadata_dict()
            # Convert datetime to string for JSON serialization
            if 'scraped_at' in metadata and metadata['scraped_at']:
                metadata['scraped_at'] = metadata['scraped_at'].isoformat()

            scrape_dict = {
                'id': scrape.id,
                'metadata': metadata,
                'content': scrape.get_content_dict(),
                'created_at': scrape.created_at.isoformat()
            }
            scrapes_data.append(scrape_dict)

        return JsonResponse(scrapes_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
