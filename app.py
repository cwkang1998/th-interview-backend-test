from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# This two is use for caching the results
cached_posts = []
cached_comments = []
cached_top_posts = []


@app.route('/top_post', methods=['GET'])
def top_post():
    global cached_posts, cached_comments, cached_top_posts
    posts_res = requests.get('https://jsonplaceholder.typicode.com/posts')
    if(posts_res.status_code == 200):
        comments_res = requests.get(
            'https://jsonplaceholder.typicode.com/comments')
        posts = posts_res.json()
        comments = comments_res.json()

        # Using length the check if the retrieved data is similar to the
        # cached data
        if not ((len(posts) == len(cached_posts))
                and (len(comments) == len(cached_comments))):
            cached_posts = posts
            cached_comments = comments
            top_posts = []
            for post in cached_posts:
                comment_count = 0
                for comment in cached_comments:
                    if(comment.get('postId', -1) == post.get('id', None)):
                        comment_count = comment_count + 1
                top_posts.append({
                    'post_id': post['id'],
                    'post_title': post['title'],
                    'post_body': post['body'],
                    'total_number_of_comments': comment_count
                })
            cached_top_posts = sorted(
                top_posts, key=lambda x: x['total_number_of_comments'])
        return jsonify(cached_top_posts), 200

    return {'error': 'Failed to get top posts'}, 400


@app.route('/search', methods=['GET'])
def search():
    return 'search'
