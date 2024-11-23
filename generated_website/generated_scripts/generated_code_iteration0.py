on
# Simplified and streamlined implementation of the IMDB-like website

from flask import Flask, jsonify, request
import psycopg2
from itertools import count
from typing import List, Dict, Optional

class Title:
    """Represent a Title with an id, name, rankings, and reviews."""

    id_generator = count(1)

    def __init__(self, name: str):
        self.id = next(Title.id_generator)
        self.name = name
        self.rankings = []
        self.reviews = []

    def add_ranking(self, ranking: int):
        if 1 <= ranking <= 10:
            self.rankings.append(ranking)

    def add_review(self, review: str):
        self.reviews.append(review)

    def average_ranking(self) -> float:
        return sum(self.rankings) / len(self.rankings) if self.rankings else 0.0

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'average_ranking': self.average_ranking(),
            'rankings': self.rankings,
            'reviews': self.reviews
        }

class DatabaseConnection:
    """Handle database connections and operations."""
    
    def __init__(self, db_config: Dict):
        self.connection = psycopg2.connect(**db_config)

    def execute_query(self, query: str, parameters: tuple = ()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

class TitleManager:
    """Manage Title data and operations in the database."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_title(self, name: str):
        new_title = Title(name)
        query = "INSERT INTO titles (id, name) VALUES (%s, %s)"
        self.db.execute_query(query, (new_title.id, new_title.name))
        self.db.commit()
        return new_title

    def get_title(self, title_id: int) -> Optional[Title]:
        query = "SELECT id, name FROM titles WHERE id = %s"
        result = self.db.execute_query(query, (title_id,))
        if result:
            title_data = result[0]
            return Title(name=title_data[1])

    def list_titles(self) -> List[Title]:
        query = "SELECT id, name FROM titles"
        results = self.db.execute_query(query)
        return [Title(name=row[1]) for row in results]

class TitleSearchService:
    """Provide search functionalities for titles."""

    def __init__(self, titles: List[Title]):
        self.titles = titles

    def search_by_name(self, name: str) -> List[Title]:
        return [title for title in self.titles if name.lower() in title.name.lower()]

    def search_suggestions(self, query: str) -> List[str]:
        suggestions = {title.name for title in self.titles if query.lower() in title.name.lower()}
        return sorted(suggestions)

class Server:
    """Application server for handling web requests."""

    def __init__(self, db_config: Dict):
        self.app = Flask(__name__)
        db = DatabaseConnection(db_config)
        self.title_manager = TitleManager(db)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/titles', methods=['GET'])
        def list_titles():
            titles = self.title_manager.list_titles()
            return jsonify([title.serialize() for title in titles])

        @self.app.route('/titles', methods=['POST'])
        def create_title():
            title_data = request.json
            new_title = self.title_manager.create_title(title_data['name'])
            return jsonify(new_title.serialize()), 201

        @self.app.route('/titles/<int:title_id>', methods=['GET'])
        def get_title(title_id):
            title = self.title_manager.get_title(title_id)
            return jsonify(title.serialize()) if title else ('', 404)

        @self.app.route('/titles/search', methods=['GET'])
        def search_titles():
            query = request.args.get('query', '')
            titles = self.title_manager.list_titles()
            search_service = TitleSearchService(titles)
            results = search_service.search_by_name(query)
            return jsonify([title.serialize() for title in results])

    def run(self):
        self.app.run(debug=True)

# Define database configuration
db_config = {
    "dbname": "your_database",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Run server
if __name__ == "__main__":
    server = Server(db_config)
    server.run()


