from flask import jsonify
from flask.views import MethodView
from utils.scraper import Scraper
from flask import request

class Filter(MethodView):

    def get (self):
        search = request.args.get('s', None)        
        if search:
            search = search.replace(' ','+')
            page_number = request.args.get('page', None)
            if not page_number:
                page_number = 1

            response = Scraper().get_filtered_series(filtered_serie=search, page=page_number)
            if not response:
                return {'info': 'Things are little unstable here. I suggest to come back later'}, 500
            return jsonify(response)
        else:
            return {'info': 'Bad request'}, 400

