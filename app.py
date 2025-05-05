from flask import Flask, render_template_string, request

from pymongo import MongoClient
 
app = Flask(__name__)
 
# Connexion MongoDB

client = MongoClient("mongodb://localhost:27017/")

db = client.blog_moderateur

collection = db.articles
 
# Template HTML avec un style moderne

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Articles par Sous-Catégorie</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>

        body { font-family: 'Inter', sans-serif; background: #f0f2f5; padding: 2rem; }

        .container { max-width: 1000px; margin: auto; }

        h1 { text-align: center; color: #333; margin-bottom: 2rem; }

        form { display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; }

        input[type=text] { padding: 0.75rem; width: 300px; border-radius: 8px; border: 1px solid #ccc; }

        button { padding: 0.75rem 1.5rem; border: none; background: #007bff; color: white; border-radius: 8px; cursor: pointer; }

        button:hover { background: #0056b3; }

        .article { background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }

        .article img { max-width: 100%; border-radius: 8px; margin-bottom: 1rem; }

        .article h3 { margin-top: 0; color: #007bff; }

        .meta { font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; }

        .resume { font-size: 1rem; color: #333; }
</style>
</head>
<body>
<div class="container">
<h1>📚 Recherche d'Articles par Sous-Catégorie</h1>
<form method="get">
<input type="text" name="categorie" placeholder="Ex: Culture web, IA, Formation..." required>
<button type="submit">Rechercher</button>
</form>
 
    {% if articles %}
<h2>{{ articles|length }} article(s) trouvé(s)</h2>

        {% for art in articles %}
<div class="article">
<h3><a href="{{ art.url }}" target="_blank">{{ art.titre }}</a></h3>
<div class="meta">🗓️ {{ art.date_pub or 'Date inconnue' }} — ✍️ {{ art.auteur or 'Auteur inconnu' }}</div>

            {% if art.thumbnail %}
<img src="{{ art.thumbnail }}" alt="Thumbnail">

            {% endif %}
<div class="resume">{{ art.resume or 'Pas de résumé disponible.' }}</div>
</div>

        {% endfor %}

    {% elif searched %}
<p>Aucun article trouvé pour cette sous-catégorie.</p>

    {% endif %}
</div>
</body>
</html>

"""
 
@app.route("/", methods=["GET"])

def index():

    categorie = request.args.get("categorie")

    searched = bool(categorie)

    articles = []
 
    if categorie:

        articles = list(collection.find({"sous_categorie": categorie}))
 
    return render_template_string(HTML_TEMPLATE, articles=articles, searched=searched)
 
if __name__ == "__main__":

    app.run(debug=True)

 