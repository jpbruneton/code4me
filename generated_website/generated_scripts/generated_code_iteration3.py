on
from flask import Flask, jsonify, request, abort
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from itertools import count
import psycopg2

# Data model for Title
@dataclass
class Title:
    id: int
    name: str
    rankings: List[int] = field(default_factory=list)
    reviews: List[str] = field(default_factory=list)

    def add_ranking(self, ranking: int):
        if 1 <= ranking <= 10:
            self.rankings.append(ranking)
        else:
            raise ValueError("Ranking must be between 1 and 10.")

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

# Database connection handler
class DatabaseConnection:
    def __init__(self, db_config: Dict):
        self.connection = psycopg2.connect(**db_config)

    def execute_query(self, query: str, parameters: tuple = (), fetch: bool = False):
        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            if fetch:
                return cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

# Manager for Title data
class TitleManager:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create_title(self, name: str) -> Title:
        title_id = next(Title.id_generator)
        query = "INSERT INTO titles (id, name) VALUES (%s, %s)"
        self.db.execute_query(query, (title_id, name))
        self.db.commit()
        return Title(id=title_id, name=name)

    def get_title(self, title_id: int) -> Optional[Title]:
        query = "SELECT id, name FROM titles WHERE id = %s"
        result = self.db.execute_query(query, (title_id,), fetch=True)
        if result:
            title = Title(id=result[0][0], name=result[0][1])
            self._load_meta_data(title)
            return title
        return None

    def list_titles(self) -> List[Title]:
        query = "SELECT id, name FROM titles"
        results = self.db.execute_query(query, fetch=True)
        return [self._populate_title(row) for row in results]

    def _populate_title(self, row) -> Title:
        title = Title(id=row[0], name=row[1])
        self._load_meta_data(title)
        return title

    def _load_meta_data(self, title: Title):
        title.rankings = self._fetch_rankings(title.id)
        title.reviews = self._fetch_reviews(title.id)

    def _fetch_rankings(self, title_id: int) -> List[int]:
        query = "SELECT ranking FROM rankings WHERE title_id = %s"
        return [r[0] for r in self.db.execute_query(query, (title_id,), fetch=True)]

    def _fetch_reviews(self, title_id: int) -> List[str]:
        query = "SELECT review FROM reviews WHERE title_id = %s"
        return [r[0] for r in self.db.execute_query(query, (title_id,), fetch=True)]

    def add_ranking(self, title_id: int, ranking: int):
        title = self.get_title(title_id)
        if not title:
            abort(404, description="Title not found.")
        title.add_ranking(ranking)
        query = "INSERT INTO rankings (title_id, ranking) VALUES (%s, %s)"
        self.db.execute_query(query, (title.id, ranking))
        self.db.commit()
    
    def add_review(self, title_id: int, review: str):
        title = self.get_title(title_id)
        if not title:
            abort(404, description="Title not found.")
        title.add_review(review)
        query = "INSERT INTO reviews (title_id, review) VALUES (%s, %s)"
        self.db.execute_query(query, (title.id, review))
        self.db.commit()

# Service to handle title search
class TitleSearchService:
    @staticmethod
    def search_by_name(titles: List[Title], name: str) -> List[Title]:
        return [title for title in titles if name.lower() in title.name.lower()]

# Flask server setup
class Server:
    def __init__(self, db_config: Dict):
        self.app = Flask(__name__)
        self.db = DatabaseConnection(db_config)
        self.title_manager = TitleManager(self.db)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/titles', methods=['GET'])
        def list_titles():
            titles = self.title_manager.list_titles()
            return jsonify([title.serialize() for title in titles])

        @self.app.route('/titles', methods=['POST'])
        def create_title():
            title_data = request.json
            if not title_data or 'name' not in title_data:
                abort(400, description="Invalid request payload.")
            new_title = self.title_manager.create_title(title_data['name'])
            return jsonify(new_title.serialize()), 201

        @self.app.route('/titles/<int:title_id>', methods=['GET'])
        def get_title(title_id):
            title = self.title_manager.get_title(title_id)
            if title is None:
                abort(404, description="Title not found.")
            return jsonify(title.serialize())

        @self.app.route('/titles/<int:title_id>/rank', methods=['POST'])
        def rank_title(title_id):
            req_data = request.json
            if not req_data or 'ranking' not in req_data:
                abort(400, description="Invalid request payload.")
            ranking = req_data['ranking']
            try:
                self.title_manager.add_ranking(title_id, ranking)
            except ValueError as e:
                abort(400, description=str(e))
            return '', 204

        @self.app.route('/titles/<int:title_id>/review', methods=['POST'])
        def review_title(title_id):
            req_data = request.json
            if not req_data or 'review' not in req_data:
                abort(400, description="Invalid request payload.")
            self.title_manager.add_review(title_id, req_data['review'])
            return '', 204

        @self.app.route('/titles/search', methods=['GET'])
        def search_titles():
            query = request.args.get('query', '')
            titles = self.title_manager.list_titles()
            results = TitleSearchService.search_by_name(titles, query)
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


