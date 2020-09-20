from flask import Flask
from views.serie import Serie
from views.page import Page
from views.episode import Episode
from views.filter import Filter
from views.video import Video

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/api/series/', view_func=Serie.as_view('series'), methods=['GET'])
    app.add_url_rule('/api/series/<dashed_title>', view_func=Serie.as_view('serie'), methods=['GET'])
    app.add_url_rule('/api/series/page/<int:page_number>', view_func=Page.as_view('page'), methods=['GET'])
    app.add_url_rule('/api/episodes/<dashed_name>', view_func=Episode.as_view('episode'), methods=['GET'])
    app.add_url_rule('/api/filter', view_func=Filter.as_view('search'), methods=['GET'])
    app.add_url_rule('/api/videos/<file_name>', view_func=Video.as_view('video'), methods=['DELETE'])
    
    return app

if __name__ == "__main__":
   app = create_app()
   app.run(debug=True)