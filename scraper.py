import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from time import sleep
 
client = MongoClient("mongodb://localhost:27017/")
db = client.blog_moderateur
collection = db.articles
 
BASE_URL = "https://www.blogdumoderateur.com"
CATEGORIE = "web"  
NB_PAGES = 10
def get_article_links_from_page(page_url):
    print(f"🔎 Lecture page : {page_url}")
    res = requests.get(page_url)
    soup = BeautifulSoup(res.text, "html.parser")
 
    articles = soup.find_all("article")
    results = []
 
    for article in articles:
        url = article.find("a", href=True)
        if not url:
            continue
 
        titre_tag = article.find("h3", class_="entry-title")
        titre = titre_tag.text.strip() if titre_tag else None
 
        categorie_tag = article.find("span", class_="favtag")
        categorie = categorie_tag.text.strip() if categorie_tag else None
 
        resume_tag = article.find("div", class_="entry-excerpt")
        resume = resume_tag.text.strip() if resume_tag else None
 
        results.append({
            "url": url["href"],
            "titre": titre,
            "sous_categorie": categorie,
            "resume": resume
        })
    return results
 
def scrape_article(article_info):
    url = article_info["url"]
    print(f"➡️ Scraping article : {url}")
 
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
 
        titre = soup.find("h1", class_="entry-title").text.strip()
 
        thumbnail_btn = soup.find("button", class_="sharing-button sharing-menu")
        thumbnail = thumbnail_btn["data-media"] if thumbnail_btn else None
 
        time_tag = soup.find("time", class_="entry-date")
        date_pub = time_tag["datetime"][:10] if time_tag else None
 
        auteur_tag = soup.find("span", class_="byline")
        auteur = auteur_tag.text.strip() if auteur_tag else None
 
        images = {}
        for figure in soup.find_all("figure"):
            img = figure.find("img")
            if img:
                src = img.get("src")
                caption = ""
                figcaption = figure.find("figcaption")
                if figcaption:
                    caption = figcaption.get_text(strip=True)
                elif img.get("alt"):
                    caption = img.get("alt")
                elif img.get("title"):
                    caption = img.get("title")
                images[src] = caption
 
        article_data = {
            "titre": titre,
            "url": url,
            "thumbnail": thumbnail,
            "sous_categorie": article_info["sous_categorie"],
            "resume": article_info["resume"],
            "date_pub": date_pub,
            "auteur": auteur,
            "images": images
        }
 
        collection.insert_one(article_data)
        print(f"Inséré : {titre}")
 
    except Exception as e:
        print(f"Erreur sur {url} : {e}")
 
for i in range(1, NB_PAGES + 1):
    page_url = f"{BASE_URL}/{CATEGORIE}/page/{i}/" if i > 1 else f"{BASE_URL}/{CATEGORIE}/"
    articles = get_article_links_from_page(page_url)
 
    for article_info in articles:
        scrape_article(article_info)
        sleep(1)  
 