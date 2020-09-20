import requests
from bs4 import BeautifulSoup
import datetime
import re
import ast
import uuid
from utils.downloader import Downloader
from utils.uploader import Uploader
import os

class Scraper:
    def get_country_of_filtered_serie(self, dashed_title):
        url = f'https://www.dramacool9.co/{dashed_title}/'
        response = requests.get(url)
        if response.status_code != 200: 
            return None      

        html = BeautifulSoup(response.text, "html.parser")  
        return html.findAll('p', {'class': 'country'})[0].contents[3].text       

    def get_filtered_series(self, filtered_serie, page): 
        part = '' if page == 1 else f'page/{page}/' 
        url = f'https://www.dramacool9.co/{part}?s={filtered_serie}'

        response = requests.get(url)        
        if response.status_code != 200:
            return None

        html = BeautifulSoup(response.text, "html.parser")
        elements = html.findAll('figure', {'class': 'post-thumbnail'})
        series = []
        
        for element in elements:
            element_sibling = element.next_sibling.next_sibling.findAll('a', string='Drama')
            if len(element_sibling) == 0:
                continue

            if len(element.contents) <= 2:
                continue            

            part = element.contents[1].attrs['href'].split('https://www.dramacool9.co/')
            dashed_title = part[1].replace('/','')  
            
            country = self.get_country_of_filtered_serie(dashed_title) 
            if country == 'Korean':      
                series.append({'dashed_title':dashed_title, 'title':element.contents[1].attrs['title'], 'cover':element.contents[1].contents[0].attrs['data-original']})
        
        return series


    def get_series(self, page = 0):
        part = '' if page == 0 else f'page/{page}/'            
        url = f'https://www.dramacool9.co/category/drama/{part}?country=korean'

        response = requests.get(url)        
        if response.status_code != 200:
            return None

        html = BeautifulSoup(response.text, "html.parser")
        elements = html.findAll('a', {'class': 'mask'})
        series = []
        
        for element in elements:
            if len(element.contents) <= 2:
                continue
            
            part = element.attrs['href'].split('https://www.dramacool9.co/')
            dashed_title = part[1].replace('/','')            
            series.append({'dashed_title':dashed_title, 'title':element.contents[1].text, 'cover':element.contents[0].attrs['data-original']})
        return series


    def get_serie(self, dashed_title): 
        url = f'https://www.dramacool9.co/{dashed_title}/'
        response = requests.get(url)
        if response.status_code != 200: 
            return None      

        html = BeautifulSoup(response.text, "html.parser")  
        serie_info = self.get_serie_info(html)
        if len(serie_info) > 0:
            serie_info['episodes']  = self.get_episodes(html)
        
        return serie_info

    def get_serie_info(self, html):
        genre_elements = html.findAll(href=re.compile('genre'))
        if not genre_elements:
            return {}                    
        genres = []            
        for genre in genre_elements:
            genres.append(genre.text)
        
        title = html.findAll('h1')[0].text
        cover = html.findAll('img', class_='lazy')[0].attrs['data-original']          
        release_year = html.findAll('p', {'class': 'release-year'})[0].contents[2].text
        about = html.findAll('p', class_='')[0].text
        status = html.findAll('p', {'class': 'status'})[0].contents[2].split('\n')[0]

        return {
            'title':title, 
            'cover':cover, 
            'release-year': release_year, 
            'about': about, 
            'status': status, 
            'genres': genres
            }


    def get_episodes(self, html):  
        title = html.findAll('h1')[0].text
        total_episodes = len(html.findAll(href=re.compile('-episode-'), title=re.compile(title)))
        episodes = []
        for n in range(total_episodes + 2):
            element = html.findAll('ul', class_='list')[0].contents[n]
            if element == '\n' or element == ' ':
                continue 
            sub_status = html.findAll('ul', class_='list')[0].contents[n].findAll('span')[0].text
            episode_url = html.findAll('ul', class_='list')[0].contents[n].findAll('a')[0].attrs['href']
            episodes.append({'url': episode_url, 'sub-status': sub_status})  
        
        episodes.reverse()
        return episodes

    def get_episode_video_file_name(self, dashed_name):
        url = f'https://www.dramacool9.co/{dashed_name}/'
        original_video_url = self.get_original_episode_video_url(url)

        path = os.path.dirname(os.path.abspath(__file__))
        file_parent_path = path.replace('utils', 'temp')
        file_name = uuid.uuid4().hex[:16] + '.mp4'
        target_file =  file_parent_path + '/' + file_name
        
        
        Downloader(url=original_video_url, file_parent_path=file_parent_path, file_name=file_name).download_file_from_source()
        uploader_tool = Uploader()
        generated_video_url_from_cloud = uploader_tool.upload_file_to_cloud(source_file_name=target_file, destination_blob_name=file_name)
        
        if generated_video_url_from_cloud:
            uploader_tool.delete_file_from_project(source_file_name=target_file)
            return file_name
            
    def get_original_episode_video_url(self, url):
        response = requests.get(url)
        if response.status_code != 200: 
            return 
        html = BeautifulSoup(response.text, "html.parser")
        fake_video_url = html.findAll(class_='serverslist')[0].attrs['data-server'].replace('streaming','ajax') + '&refer=none'
      
        headers = requests.utils.default_headers()
        headers.update({
            'X-Requested-With': 'XMLHttpRequest',
        })

        response = requests.get(fake_video_url, headers=headers)
        if response.status_code != 200: 
            return 
        html = BeautifulSoup(response.text, "html.parser")          
        content_in_dict = ast.literal_eval(str(html))
        return content_in_dict['source'][0]['file'].replace('\\','')
