on
from flask import Flask, jsonify, request, abort
import psycopg2
from itertools import count
from typing import List, Dict, Optional

class Title:
    """Represents a media title with its rankings and reviews."""
    
    id_generator = count(1)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.rankings = []
        self.reviews = []

    def add_ranking(self, ranking: int):
        """Add a ranking score to the title."""
        if 1 <= ranking <= 10:
            self.rankings.append(ranking)
        else:
            raise ValueError("Ranking must be between 1 and 10.")

    def add_review(self, review: str):
        """Add a text review to the title."""
        self.reviews.append(review)

    def average_ranking(self) -> float:
        """Calculate and return the average ranking."""
        return sum(self.rankings) / len(self.rankings) if self.rankings else 0.0

    def serialize(self) -> Dict:
        """Return a dictionary representation of the title."""
        return {
            'id': self.id,
            'name': self.name,
            'average_ranking': self.average_ranking(),
            'rankings': self.rankings,
            'reviews': self.reviews
        }

class DatabaseConnection:
    """Manages database connections and operations."""
    
    def __init__(self, db_config: Dict):
        self.connection = psycopg2.connect(**db_config)

    def execute_query(self, query: str, parameters: tuple = (), fetch: bool = False):
        """Execute a database query with optional fetching of results."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            if fetch:
                return cursor.fetchall()

    def commit(self):
        """Commit the current transaction."""
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()

class TitleManager:
    """Handles CRUD operations for titles in the database."""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_title(self, name: str) -> Title:
        """Create a new title in the database."""
        title_id = next(Title.id_generator)
        query = "INSERT INTO titles (id, name) VALUES (%s, %s)"
        self.db.execute_query(query, (title_id, name))
        self.db.commit()
        return Title(id=title_id, name=name)

    def get_title(self, title_id: int) -> Optional[Title]:
        """Retrieve a title from the database by its ID."""
        query = "SELECT id, name FROM titles WHERE id = %s"
        result = self.db.execute_query(query, (title_id,), fetch=True)
        if result:
            title_data = result[0]
            title = Title(id=title_data[0], name=title_data[1])
            self._load_meta_data(title)
            return title
        return None

    def list_titles(self) -> List[Title]:
        """List all titles in the database."""
        query = "SELECT id, name FROM titles"
        results = self.db.execute_query(query, fetch=True)
        titles = [Title(id=row[0], name=row[1]) for row in results]
        for title in titles:
            self._load_meta_data(title)
        return titles

    def _load_meta_data(self, title: Title):
        """Load rankings and reviews for a title."""
        ranking_query = "SELECT ranking FROM rankings WHERE title_id = %s"
        rankings = self.db.execute_query(ranking_query, (title.id,), fetch=True)
        title.rankings = [r[0] for r in rankings]

        review_query = "SELECT review FROM reviews WHERE title_id = %s"
        reviews = self.db.execute_query(review_query, (title.id,), fetch=True)
        title.reviews = [r[0] for r in reviews]

    def add_ranking(self, title_id: int, ranking: int):
        """Add a ranking to a title."""
        title = self.get_title(title_id)
        if not title:
            abort(404, description="Title not found.")
        title.add_ranking(ranking)
        query = "INSERT INTO rankings (title_id, ranking) VALUES (%s, %s)"
        self.db.execute_query(query, (title.id, ranking))
        self.db.commit()

    def add_review(self, title_id: int, review: str):
        """Add a review to a title."""
        title = self.get_title(title_id)
        if not title:
            abort(404, description="Title not found.")
        title.add_review(review)
        query = "INSERT INTO reviews (title_id, review) VALUES (%s, %s)"
        self.db.execute_query(query, (title.id, review))
        self.db.commit()

class TitleSearchService:
    """Handles search functionalities for titles."""
    
    @staticmethod
    def search_by_name(titles: List[Title], name: str) -> List[Title]:
        """Search for titles by name."""
        return [title for title in titles if name.lower() in title.name.lower()]

class Server:
    """Flask server for handling API requests."""
    
    def __init__(self, db_config: Dict):
        self.app = Flask(__name__)
        self.db = DatabaseConnection(db_config)
        self.title_manager = TitleManager(self.db)
        self.setup_routes()

    def setup_routes(self):
        """Setup Flask routes for the API."""

        @self.app.route('/titles', methods=['GET'])
        def list_titles():
            """Get a list of all titles."""
            titles = self.title_manager.list_titles()
            return jsonify([title.serialize() for title in titles])

        @self.app.route('/titles', methods=['POST'])
        def create_title():
            """Create a new title."""
            title_data = request.json
            if not title_data or 'name' not in title_data:
                abort(400, description="Invalid request payload.")
            new_title = self.title_manager.create_title(title_data['name'])
            return jsonify(new_title.serialize()), 201

        @self.app.route('/titles/<int:title_id>', methods=['GET'])
        def get_title(title_id):
            """Get a specific title by ID."""
            title = self.title_manager.get_title(title_id)
            if title is None:
                abort(404, description="Title not found.")
            return jsonify(title.serialize())

        @self.app.route('/titles/<int:title_id>/rank', methods=['POST'])
        def rank_title(title_id):
            """Add a ranking to a title."""
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
            """Add a review to a title."""
            req_data = request.json
            if not req_data or 'review' not in req_data:
                abort(400, description="Invalid request payload.")
            review = req_data['review']
            self.title_manager.add_review(title_id, review)
            return '', 204

        @self.app.route('/titles/search', methods=['GET'])
        def search_titles():
            """Search for titles by query string."""
            query = request.args.get('query', '')
            titles = self.title_manager.list_titles()
            results = TitleSearchService.search_by_name(titles, query)
            return jsonify([title.serialize() for title in results])

    def run(self):
        """Run the Flask application."""
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


