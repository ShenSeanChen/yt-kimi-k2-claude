import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import json
from typing import List, Dict, Any

class WebScraper:
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            time.sleep(self.delay)
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_quotes(self, pages: int = 1) -> List[Dict[str, Any]]:
        """Scrape quotes from quotes.toscrape.com"""
        quotes_data = []
        
        for page in range(1, pages + 1):
            url = f"http://quotes.toscrape.com/page/{page}/"
            soup = self.get_page(url)
            
            if not soup:
                continue
            
            quotes = soup.find_all('div', class_='quote')
            
            for quote in quotes:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
                
                quotes_data.append({
                    'text': text,
                    'author': author,
                    'tags': tags,
                    'tags_count': len(tags)
                })
        
        return quotes_data
    
    def scrape_github_trending(self, language: str = 'python') -> List[Dict[str, Any]]:
        """Scrape GitHub trending repositories"""
        url = f"https://github.com/trending/{language}"
        soup = self.get_page(url)
        
        if not soup:
            return []
        
        repos = soup.find_all('article', class_='Box-row')
        repos_data = []
        
        for repo in repos:
            try:
                name_elem = repo.find('h2', class_='h3').find('a')
                name = name_elem.get_text().strip().replace('\n', '').replace(' ', '')
                
                description_elem = repo.find('p', class_='col-9')
                description = description_elem.get_text().strip() if description_elem else "No description"
                
                stars_elem = repo.find('span', class_='d-inline-block float-sm-right')
                stars = stars_elem.get_text().strip() if stars_elem else "0"
                
                language_elem = repo.find('span', itemprop='programmingLanguage')
                language_name = language_elem.get_text().strip() if language_elem else "Unknown"
                
                repos_data.append({
                    'name': name,
                    'description': description,
                    'stars': stars,
                    'language': language_name
                })
            except Exception as e:
                print(f"Error parsing repo: {e}")
                continue
        
        return repos_data
    
    def scrape_table_data(self, url: str) -> pd.DataFrame:
        """Scrape tabular data from a webpage"""
        soup = self.get_page(url)
        if not soup:
            return pd.DataFrame()
        
        tables = pd.read_html(str(soup))
        return tables[0] if tables else pd.DataFrame()

class DataProcessor:
    @staticmethod
    def process_quotes_data(quotes: List[Dict[str, Any]]) -> pd.DataFrame:
        """Process quotes data into a pandas DataFrame"""
        df = pd.DataFrame(quotes)
        
        # Explode tags to create separate rows
        df_exploded = df.explode('tags')
        
        # Create additional features
        df['text_length'] = df['text'].str.len()
        df['word_count'] = df['text'].str.split().str.len()
        
        return df, df_exploded
    
    @staticmethod
    def process_github_data(repos: List[Dict[str, Any]]) -> pd.DataFrame:
        """Process GitHub data into a pandas DataFrame"""
        df = pd.DataFrame(repos)
        
        # Clean stars data
        df['stars'] = df['stars'].str.replace(',', '').astype(float)
        
        # Create additional features
        df['description_length'] = df['description'].str.len()
        df['name_length'] = df['name'].str.len()
        
        return df

class Visualizer:
    @staticmethod
    def create_quotes_visualizations(df: pd.DataFrame, df_exploded: pd.DataFrame):
        """Create visualizations for quotes data"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Top authors by quote count
        author_counts = df['author'].value_counts().head(10)
        axes[0, 0].bar(author_counts.index, author_counts.values)
        axes[0, 0].set_title('Top 10 Authors by Quote Count')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Tags distribution
        tag_counts = df_exploded['tags'].value_counts().head(10)
        axes[0, 1].bar(tag_counts.index, tag_counts.values)
        axes[0, 1].set_title('Top 10 Tags')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Text length distribution
        axes[1, 0].hist(df['text_length'], bins=20, edgecolor='black')
        axes[1, 0].set_title('Distribution of Quote Text Length')
        axes[1, 0].set_xlabel('Character Count')
        axes[1, 0].set_ylabel('Frequency')
        
        # Tags count vs text length scatter
        axes[1, 1].scatter(df['tags_count'], df['text_length'], alpha=0.6)
        axes[1, 1].set_title('Tags Count vs Text Length')
        axes[1, 1].set_xlabel('Number of Tags')
        axes[1, 1].set_ylabel('Text Length')
        
        plt.tight_layout()
        plt.savefig('quotes_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def create_github_visualizations(df: pd.DataFrame):
        """Create visualizations for GitHub data"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Stars distribution
        axes[0, 0].hist(df['stars'], bins=20, edgecolor='black')
        axes[0, 0].set_title('Distribution of Repository Stars')
        axes[0, 0].set_xlabel('Stars')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_yscale('log')
        
        # Top repositories by stars
        top_repos = df.nlargest(10, 'stars')
        axes[0, 1].barh(top_repos['name'], top_repos['stars'])
        axes[0, 1].set_title('Top 10 Repositories by Stars')
        axes[0, 1].set_xlabel('Stars')
        
        # Description length vs stars
        axes[1, 0].scatter(df['description_length'], df['stars'], alpha=0.6)
        axes[1, 0].set_title('Description Length vs Stars')
        axes[1, 0].set_xlabel('Description Length')
        axes[1, 0].set_ylabel('Stars')
        axes[1, 0].set_yscale('log')
        
        # Language distribution
        lang_counts = df['language'].value_counts()
        axes[1, 1].pie(lang_counts.values, labels=lang_counts.index, autopct='%1.1f%%')
        axes[1, 1].set_title('Distribution by Programming Language')
        
        plt.tight_layout()
        plt.savefig('github_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Main function to run the complete pipeline"""
    print("Starting web scraping pipeline...")
    
    # Initialize scraper
    scraper = WebScraper(delay=1.0)
    
    # Scrape quotes data
    print("Scraping quotes data...")
    quotes_data = scraper.scrape_quotes(pages=5)
    
    if quotes_data:
        # Process quotes data
        print("Processing quotes data...")
        quotes_df, quotes_exploded = DataProcessor.process_quotes_data(quotes_data)
        
        # Save to CSV
        quotes_df.to_csv('quotes_data.csv', index=False)
        quotes_exploded.to_csv('quotes_exploded.csv', index=False)
        
        # Create visualizations
        print("Creating visualizations...")
        Visualizer.create_quotes_visualizations(quotes_df, quotes_exploded)
        
        print(f"Quotes analysis complete! Processed {len(quotes_df)} quotes.")
    
    # Scrape GitHub trending data
    print("Scraping GitHub trending repositories...")
    github_data = scraper.scrape_github_trending('python')
    
    if github_data:
        # Process GitHub data
        print("Processing GitHub data...")
        github_df = DataProcessor.process_github_data(github_data)
        
        # Save to CSV
        github_df.to_csv('github_trending.csv', index=False)
        
        # Create visualizations
        Visualizer.create_github_visualizations(github_df)
        
        print(f"GitHub analysis complete! Processed {len(github_df)} repositories.")
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()