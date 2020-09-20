from flask.views import MethodView
from utils.scraper import Scraper

class Episode(MethodView):
    
    def get(self, dashed_name=None):
        response = Scraper().get_episode_video_file_name(dashed_name)        
        if not response:
            return {'info': 'Things are little unstable here. I suggest to come back later'}, 500
        return {'file-name':response}