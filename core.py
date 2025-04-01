import praw
import pandas as pd
import datetime
import os
import time
import logging
from dotenv import load_dotenv
from typing import Dict, Any

# Configuration du logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("reddit_tech_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("RedditTechBot")

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

class RedditTechBot:
    def __init__(self):
        # Configuration de l'API Reddit
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'TechWatchBot v1.0')
        )
        
        # Liste des subreddits technologiques à surveiller
        self.tech_subreddits = [
            'technology', 'programming', 'webdev', 'MachineLearning', 
            'cybersecurity', 'devops', 'python', 'javascript',
            'artificialintelligenc', 'cloudcomputing', 'datascience'
        ]
        
        # Création du dossier pour sauvegarder les données
        self.data_folder = "tech_watch_data"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            
        logger.info("RedditTechBot initialisé avec succès")
    
    def translate_and_summarize(self, text: str, title: str) -> Dict[str, str]:
        """Traduit et résume un article en français"""
        try:
            if not text:
                text = title
                
            prompt = f"""Article: {title}
            Content: {text}
            
            Traduisez le titre et le contenu en français, puis faites un résumé concis.
            Format de réponse souhaité:
            Titre traduit: <titre en français>
            Résumé: <résumé en français de 2-3 phrases>
            """
            
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Vous êtes un traducteur et rédacteur professionnel français."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            
            # Extraire le titre traduit et le résumé
            title_trans = result.split("Titre traduit:")[1].split("Résumé:")[0].strip()
            summary = result.split("Résumé:")[1].strip()
            
            return {
                "translated_title": title_trans,
                "summary": summary
            }
        except Exception as e:
            logger.error(f"Erreur lors de la traduction/résumé: {e}")
            return {
                "translated_title": title,
                "summary": "Erreur lors de la génération du résumé"
            }

    def get_top_posts(self, subreddit_name, time_filter='day', limit=25):
        """Récupère les meilleurs posts d'un subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for post in subreddit.top(time_filter=time_filter, limit=limit):
                posts.append({
                    'subreddit': subreddit_name,
                    'title': post.title,
                    'score': post.score,
                    'url': post.url,
                    'post_url': f"https://www.reddit.com{post.permalink}",
                    'created_utc': datetime.datetime.fromtimestamp(post.created_utc),
                    'num_comments': post.num_comments,
                    'author': str(post.author),
                    'selftext': post.selftext[:500] + '...' if len(post.selftext) > 500 else post.selftext
                })
            
            logger.info(f"Récupéré {len(posts)} posts de r/{subreddit_name}")
            return posts
        
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des posts de r/{subreddit_name}: {e}")
            return []
    
    def collect_tech_news(self, time_filter='day', limit=25):
        """Collecte les nouvelles technologiques de tous les subreddits configurés"""
        all_posts = []
        
        for subreddit in self.tech_subreddits:
            posts = self.get_top_posts(subreddit, time_filter, limit)
            all_posts.extend(posts)
            # Pause pour respecter les limites d'API de Reddit
            time.sleep(2)
        
        # Créer un DataFrame avec tous les posts
        df = pd.DataFrame(all_posts)
        
        # Trier par score (popularité)
        if not df.empty:
            df.sort_values(by='score', ascending=False, inplace=True)
        
        return df
    
    def save_to_csv(self, df, filename=None):
        """Sauvegarde les données dans un fichier CSV"""
        if df.empty:
            logger.warning("Aucune donnée à sauvegarder")
            return
        
        if filename is None:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"tech_news_{current_date}.csv"
        
        file_path = os.path.join(self.data_folder, filename)
        df.to_csv(file_path, index=False, encoding='utf-8')
        logger.info(f"Données sauvegardées dans {file_path}")
        
        return file_path
    
    def generate_report(self, df, top_n=50):
        """Génère un rapport HTML des meilleures actualités technologiques"""
        if df.empty:
            logger.warning("Aucune donnée pour générer un rapport")
            return None
        
        # Limiter aux top_n posts
        df_top = df.head(top_n)
        
        # Créer le rapport HTML
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        html_file = os.path.join(self.data_folder, f"tech_report_{current_date}.html")
        
        # En-tête HTML avec un peu de style
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Veille Technologique - {current_date}</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333366; }}
                h2 {{ color: #336699; margin-top: 30px; }}
                .post {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .post-title {{ font-weight: bold; font-size: 18px; }}
                .post-meta {{ color: #666; font-size: 14px; margin: 5px 0; }}
                .post-content {{ margin-top: 10px; }}
                .source {{ font-style: italic; color: #888; }}
            </style>
        </head>
        <body>
            <h1>Veille Technologique - {current_date}</h1>
            <p>Rapport généré automatiquement des {top_n} meilleures actualités technologiques sur Reddit.</p>
        """
        
        # Modifier la partie qui génère chaque post
        for i, row in df_top.iterrows():
            html_content += f"""
            <div class="post">
                <div class="post-title">
                    <a href="{row['post_url']}" target="_blank">{row['title']}</a>
                </div>
                <div class="post-meta">
                    Score: {row['score']} | Commentaires: {row['num_comments']} | 
                    Date: {row['created_utc'].strftime("%Y-%m-%d %H:%M")}
                </div>
                <div class="source">Source: r/{row['subreddit']} | Auteur: {row['author']}</div>
                <div class="post-content">
                    {row['selftext'] if row['selftext'] else '<a href="' + row['url'] + '" target="_blank">Lien vers le contenu externe</a>'}
                </div>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        # Enregistrer le fichier HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Rapport HTML généré dans {html_file}")
        return html_file

    def run_daily_collection(self):
        """Exécute la collecte quotidienne des actualités technologiques"""
        logger.info("Démarrage de la collecte quotidienne")
        df = self.collect_tech_news(time_filter='day')
        self.save_to_csv(df)
        report_path = self.generate_report(df)
        logger.info(f"Collecte quotidienne terminée. Rapport disponible: {report_path}")
        return report_path


if __name__ == "__main__":
    bot = RedditTechBot()
    
    # Exemple d'utilisation pour exécuter une collecte unique
    report_path = bot.run_daily_collection()
    print(f"Rapport généré: {report_path}")
    
    # Pour une exécution programmée, vous pourriez utiliser un programmeur comme schedule:
    """
    import schedule
    
    def job():
        bot = RedditTechBot()
        bot.run_daily_collection()
    
    # Programmer l'exécution tous les jours à 8h00
    schedule.every().day.at("08:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifier toutes les minutes
    """