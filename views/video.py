from flask.views import MethodView
from utils.uploader import Uploader

class Video(MethodView):

    def delete (self, file_name):
        Uploader().delete_file_from_cloud(file_name)
        return {'info': 'Done'}

