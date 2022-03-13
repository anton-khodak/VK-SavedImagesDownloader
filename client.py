import math
from typing import List

import vk_api


class Photo:

    def __init__(self, url, date):
        self.url = url
        self.date = date

class User(object):
    '''VK user class.'''

    def __init__(self, token):
        self.access_token = token

    def auth(self):
        '''Authorizing user with access to photos.'''

        session = vk_api.VkApi(token=self.access_token)
        api = session.get_api()
        return api

    def get_photos(self, api) -> List[Photo]:
        '''Get list of saved photos URL's.'''

        albums = api.photos.getAlbums(need_system=1)["items"]
        saved_photos = [x for x in albums if x["id"] == -15][0]
        photos_count = saved_photos["size"]

        print("You've got {} saved photos!".format(photos_count))
        photos = []

        for i in range(math.ceil(photos_count / 1000)):
            saved_photos = api.photos.get(album_id="saved", count=1000, offset=i*1000)
            for photo in saved_photos["items"]:
                photo_resolutions = sorted(photo['sizes'], key=lambda x: x['height'], reverse=True)
                photos.append(Photo(photo_resolutions[0]['url'], photo['date']))

        return photos

    def get_credentials(self, api):
        '''Get current user's name and last name.'''

        first_name = api.users.get()[0]["first_name"]
        last_name = api.users.get()[0]["last_name"]
        return (first_name, last_name)
