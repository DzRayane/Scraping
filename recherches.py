from pymongo import MongoClient
 
client = MongoClient("mongodb://localhost:27017/")
db = client.blog_moderateur
collection = db.articles
 
def chercher_articles_par_sous_categorie(categorie):
    print(f"\n Articles dans la sous-catégorie : {categorie}")
    resultats = collection.find({"sous_categorie": categorie})
 
    count = 0
    for article in resultats:
        print(f"\n {article['titre']}")
        print(f"Date : {article.get('date_pub', 'inconnue')}")
        print(f"Auteur : {article.get('auteur', 'inconnu')}")
        print(f" Lien : {article['url']}")
        count += 1
 
    if count == 0:
        print("Aucun article trouvé.")
 
if __name__ == "__main__":
    categorie_recherchee = input("Entrez la sous-catégorie à rechercher (ex: Culture web, IA, Social...) : ")
    chercher_articles_par_sous_categorie(categorie_recherchee.strip())
 
 