# Reddit Tech Watch Bot 🤖

## Description
Un bot Python qui surveille automatiquement les principales actualités technologiques sur Reddit. Le bot collecte les posts les plus populaires, génère des rapports HTML et peut traduire le contenu en français.

## Fonctionnalités 🚀
- Surveillance de 11 subreddits tech populaires
- Collecte quotidienne automatisée des meilleurs posts
- Traduction et résumé automatique en français (via OpenAI GPT-3.5)
- Génération de rapports HTML consultables
- Export des données en CSV
- Système de logging complet

## Installation 🛠️

### Prérequis
```bash
Python 3.7+
pip install praw pandas python-dotenv openai schedule
```

### Configuration
1. Clonez le repository
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `.env` à la racine :
```plaintext
REDDIT_CLIENT_ID=votre_client_id
REDDIT_CLIENT_SECRET=votre_client_secret
REDDIT_USER_AGENT=TechWatchBot v1.0
OPENAI_API_KEY=votre_clé_api_openai
```

## Utilisation 💻

### Exécution simple
```python
from core import RedditTechBot

bot = RedditTechBot()
report_path = bot.run_daily_collection()
print(f"Rapport généré: {report_path}")
```

### Exécution programmée
```python
import schedule
from core import RedditTechBot

def job():
    bot = RedditTechBot()
    bot.run_daily_collection()

# Exécution tous les jours à 8h00
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Subreddits surveillés 📱
- technology
- programming
- webdev
- MachineLearning
- cybersecurity
- devops
- python
- javascript
- artificialintelligence
- cloudcomputing
- datascience

## Structure des données 📊

### Posts collectés
- Titre
- Score (upvotes)
- URL
- Nombre de commentaires
- Auteur
- Contenu textuel
- Date de création
- Traduction en français
- Résumé en français

### Fichiers générés
- Rapports HTML : `tech_watch_data/tech_report_YYYY-MM-DD.html`
- Données CSV : `tech_watch_data/tech_news_YYYY-MM-DD.csv`
- Logs : `reddit_tech_bot.log`

## Structure du projet 📁
```
reddit-tech-watch/
│
├── core.py           # Code principal du bot
├── .env             # Configuration (à créer)
├── requirements.txt  # Dépendances
└── tech_watch_data/ # Dossier des rapports
    ├── tech_report_*.html
    └── tech_news_*.csv
```

## Configuration du logging 📝
Le bot utilise le module logging de Python pour tracer son activité :
- Niveau : INFO
- Format : Horodatage + Nom + Niveau + Message
- Sortie : Fichier + Console

## Fonctionnalités détaillées ⚙️

### Collecte des posts
- Récupération des meilleurs posts des dernières 24h
- Limite de 25 posts par subreddit
- Délai de 2 secondes entre chaque requête (respect des limites API)

### Traduction et résumé
- Traduction automatique des titres en français
- Génération de résumés concis en français
- Utilisation de l'API OpenAI GPT-3.5

### Génération de rapports
- Format HTML responsive
- Classement par popularité
- Liens directs vers les posts originaux
- Affichage des métadonnées importantes

## Contribution 🤝
Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/NouvelleFeature`)
3. Commit vos changements (`git commit -m 'Ajout: nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/NouvelleFeature`)
5. Ouvrir une Pull Request

## Licence 📄
Ce projet est sous licence MIT.

## Auteur ✨
Aslmov
koumana-morguen-portfolio.vercel.app/works