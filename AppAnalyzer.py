# app_review_analyzer.py

from google_play_scraper import Sort, search, reviews
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download necessary NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')


class AppReviewAnalyzer:

    def __init__(self):
        # Define keywords for all factors
        self.security_keywords = ['security', 'privacy', 'data breach', 'safe', 'secure', 'hacking', 'protection']
        self.ui_keywords = ['UI', 'interface', 'design', 'navigation', 'user-friendly', 'experience', 'layout']
        self.accessibility_keywords = ['accessibility', 'empathy', 'support', 'help', 'disability', 'inclusive',
                                       'assist']
        self.response_time_keywords = ['response', 'fast', 'quick', 'lag', 'slow', 'delay', 'performance', 'loading']
        self.personalization_keywords = ['personalization', 'customize', 'preferences', 'settings', 'adaptable',
                                         'tailored']
        self.convenience_keywords = ['convenient', 'easy', 'quick', 'efficient', 'time-saving', 'effortless',
                                     'accessible']
        self.value_keywords = ['value', 'worth', 'price', 'affordable', 'expensive', 'cost', 'cheap', 'quality-price']
        self.simplicity_keywords = ['simple', 'easy', 'intuitive', 'minimal', 'straightforward', 'clean']
        self.quality_keywords = ['quality', 'performance', 'functionality', 'stability', 'efficiency', 'reliable']

    def preprocess_text(self, text):
        """Preprocess the text: lowercase, tokenize, remove stopwords, and punctuation."""
        # Convert to lowercase
        text = text.lower()

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove punctuation
        tokens = [word for word in tokens if word.isalnum()]

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        return tokens

    def categorize_review(self, text):
        """Categorize the review based on the defined keywords."""
        tokens = self.preprocess_text(text)

        if any(keyword in tokens for keyword in self.security_keywords):
            return 'Security'
        elif any(keyword in tokens for keyword in self.ui_keywords):
            return 'UI'
        elif any(keyword in tokens for keyword in self.accessibility_keywords):
            return 'Accessibility/Empathy'
        elif any(keyword in tokens for keyword in self.response_time_keywords):
            return 'Response Time'
        elif any(keyword in tokens for keyword in self.personalization_keywords):
            return 'Personalization'
        elif any(keyword in tokens for keyword in self.convenience_keywords):
            return 'Convenience'
        elif any(keyword in tokens for keyword in self.value_keywords):
            return 'Value'
        elif any(keyword in tokens for keyword in self.simplicity_keywords):
            return 'Simplicity'
        elif any(keyword in tokens for keyword in self.quality_keywords):
            return 'Quality'
        else:
            return 'Other'

    def fetch_and_categorize_reviews(self, app_id, n_reviews=5000):
        """Fetch reviews for an app and categorize them."""
        try:
            # Fetch reviews
            g_reviews, _ = reviews(
                app_id,
                lang='en',  # defaults to 'en'
                country='in',  # defaults to 'us'
                sort=Sort.NEWEST,
                count=n_reviews
            )
            # Convert to DataFrame
            reviews_df = pd.DataFrame(g_reviews)
            d = reviews_df
            print(d)
            d.to_excel('output.xlsx', index=False)
            # Categorize reviews based on keywords
            reviews_df['category'] = reviews_df['content'].apply(self.categorize_review)

            return reviews_df
        except Exception as e:
            print(f"Error fetching reviews for {app_id}: {e}")
            return pd.DataFrame()

    def analyze_review_categories(self, reviews_df):
        """Analyze the proportions of reviews in each category."""
        total_reviews = len(reviews_df)
        if total_reviews == 0:
            return {factor: 0 for factor in
                    ['Security', 'UI', 'Accessibility/Empathy', 'Response Time', 'Personalization', 'Convenience',
                     'Value', 'Simplicity', 'Quality', 'Other']}

        category_counts = reviews_df['category'].value_counts(normalize=True).to_dict()
        return {
            "Security": category_counts.get("Security", 0) * 100,
            "UI": category_counts.get("UI", 0) * 100,
            "Accessibility/Empathy": category_counts.get("Accessibility/Empathy", 0) * 100,
            "Response Time": category_counts.get("Response Time", 0) * 100,
            "Personalization": category_counts.get("Personalization", 0) * 100,
            "Convenience": category_counts.get("Convenience", 0) * 100,
            "Value": category_counts.get("Value", 0) * 100,
            "Simplicity": category_counts.get("Simplicity", 0) * 100,
            "Quality": category_counts.get("Quality", 0) * 100,
            "Other": category_counts.get("Other", 0) * 100
        }

    def analyze_apps(self, keyword):
        """Search for apps based on a keyword and analyze reviews for each app."""
        # Search for apps in the Google Play Store
        result = search(
            keyword,
            lang="en",  # defaults to 'en'
            country="in",  # defaults to 'us'
            n_hits=10  # defaults to 30 (= Google's maximum)
        )

        # Store search results
        search_results = pd.DataFrame(result)

        all_app_data = []
        for idx, row in search_results.iterrows():
            app_id = row['appId']
            app_name = row['title']

            print(f"Analyzing app: {app_name} ({app_id})")

            # Fetch and categorize reviews
            reviews_df = self.fetch_and_categorize_reviews(app_id)

            # Analyze the categorized reviews
            analysis = self.analyze_review_categories(reviews_df)
            analysis['app_name'] = app_name
            analysis['app_id'] = app_id

            all_app_data.append(analysis)

        # Convert analysis results to DataFrame
        analysis_df = pd.DataFrame(all_app_data)

        return analysis_df

    def rank_apps_by_categories(self, analysis_df):
        """Rank apps based on their scores in each category."""
        categories = ['Security', 'UI', 'Accessibility/Empathy', 'Response Time', 'Personalization', 'Convenience',
                      'Value', 'Simplicity', 'Quality']

        # Create a DataFrame to store rankings
        rank_df = pd.DataFrame()

        for category in categories:
            rank_df[category] = analysis_df[category].rank(ascending=False,
                                                           method='min')  # Rank in descending order (higher percentage is better)

        # Calculate total rank for each app (sum of ranks across categories)
        analysis_df['Total Rank'] = rank_df.sum(axis=1)

        # Find the app with the lowest total rank
        best_app = analysis_df.loc[analysis_df['Total Rank'].idxmin()]

        return best_app

    def suggest_best_app(self, analysis_df):
        """Suggest the best app based on overall rank."""
        best_app = self.rank_apps_by_categories(analysis_df)

        print("\nBest Overall App:")
        print(f"App Name: {best_app['app_name']}")
        print(f"Total Rank (lower is better): {best_app['Total Rank']}")

        for category in ['Security', 'UI', 'Accessibility/Empathy', 'Response Time', 'Personalization', 'Convenience',
                         'Value', 'Simplicity', 'Quality']:
            print(f"{category} Score: {best_app[category]}%")

        return best_app
