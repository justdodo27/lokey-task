from datetime import datetime

from http import HTTPStatus

from connexion import NoContent, request

from lib.models import Article, db


def get(user):
    year = request.args.to_dict().get("year", None)
    if year:
        articles = Article.query.filter(
            Article.author_user_id == user['user_id']
        ).filter(
            Article.created_at.between(f'{year}-01-01', f'{year}-12-31')
        ).all()
    else:
        articles = Article.query.filter(
            Article.author_user_id == user['user_id']
        ).all()

    return [
       {
           'article_id': article.article_id,
           'title': article.title,
           'content': article.content,
           'created_at': article.created_at
       }
       for article in articles
    ], HTTPStatus.OK


def post(user, body):
    db.session.add(Article(
        author_user_id=user['user_id'],
        title=body['title'],
        content=body['content'],
        created_at= datetime.strptime(body['created_at'], "%a, %d %b %Y %H:%M:%S %Z")
    ))
    db.session.commit()

    return NoContent, HTTPStatus.OK


def put(user, article_id, body):
    article = Article.query.filter(
        Article.article_id == article_id,
        Article.author_user_id == user['user_id'],
    ).first()

    if not article:
        return NoContent, HTTPStatus.NOT_FOUND

    article.title = body['title']
    article.content = body['content']
    article.created_at = datetime.strptime(body['created_at'], "%a, %d %b %Y %H:%M:%S %Z")
    db.session.commit()

    return NoContent, HTTPStatus.OK


def delete(user, article_id):
    Article.query.filter(
        Article.article_id == article_id,
        Article.author_user_id == user['user_id'],
    ).delete()

    db.session.commit()

    return NoContent, HTTPStatus.OK


