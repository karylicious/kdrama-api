from flask import jsonify
from flask.views import MethodView
from utils.scraper import Scraper

class Serie(MethodView):
    
    def get(self, dashed_title=None):        
        scraper = Scraper()        
        response = scraper.get_serie(dashed_title) if dashed_title else scraper.get_series()        
        if not response:
            return {'info': 'Things are little unstable here. I suggest to come back later'}, 500
        return jsonify(response)