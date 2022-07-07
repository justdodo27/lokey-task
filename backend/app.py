from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title: str, content: str, created_at):
        self.title = title
        self.content = content
        self.created_at = created_at
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/api/article', methods = ['GET', 'POST'])
def handle_create_read():
    if request.method == 'GET':
        if request.data:
            data = request.json
            if year := data.get("year_of_release", None):
                articles = Article.query.filter(Article.created_at.between(f'{year}-01-01', f'{year}-12-31')).all()
                return {"articles": [article.as_dict() for article in articles]}, 200
            else:
                return {"info": "Missing year_of_release"}, 400
                
        else:
            articles = Article.query.all()
            response = jsonify({"articles": [article.as_dict() for article in articles]})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200
    elif request.method == "POST":
        if request.data:
            data = request.json
            title = data.get("title", None)
            if title is None or len(title) == 0:
                return {"info": "title not provided"}, 400
            content = data.get("content", None)
            if content is None or len(content) == 0:
                return {"info": "content not provided"}, 400
            created_at = data.get("created_at", None)
            if created_at is not None:
                try:
                    created_at = datetime.strptime(created_at, "%a, %d %b %Y %H:%M:%S %Z")
                except ValueError:
                    return {"info": "wrong datetime format"}, 400
            article = Article(title, content, created_at)
            db.session.add(article)
            db.session.commit()
            return {"article": article.as_dict()}, 200
        else:
            return {"info": "no data provided"}, 400

@app.route('/api/article/<int:id>/', methods=["DELETE", "PUT"])
def handle_update_delete(id):
    if request.method == "PUT":
        if article := Article.query.filter_by(id=id).first():
            if request.data:
                data = request.json
                title = data.get("title", None)
                if title is None or len(title) == 0:
                    return {"info": "title not provided"}, 400
                content = data.get("content", None)
                if content is None or len(content) == 0:
                    return {"info": "content not provided"}, 400
                created_at = data.get("created_at", None)
                if created_at is None:
                    return {"info": "created_at not provided"}, 400
                try:
                    created_at = datetime.strptime(created_at, "%a, %d %b %Y %H:%M:%S %Z")
                except ValueError:
                    return {"info": "wrong datetime format"}, 400
                article.title = title
                article.content = content
                article.created_at = created_at
                db.session.commit()
                return {"article": article.as_dict()}, 200
            else:
                return {"info": "no data provided"}, 400
        else:
            return {"info": f"article with id {id} not found"}, 404
    elif request.method == "DELETE":
        if article := Article.query.filter_by(id=id).first():
            db.session.delete(article)
            db.session.commit()
            return {"info": "success"}, 200
        else:
            return {"info": f"article with id {id} not found"}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)