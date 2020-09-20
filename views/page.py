from flask import jsonify
from flask.views import MethodView
from utils.scraper import Scraper

class Page(MethodView):
    
    def get(self, page_number):
        response = Scraper().get_series(page=page_number)        
        if not response:
            return {'info': 'Things are little unstable here. I suggest to come back later'}, 500
        return jsonify(response)