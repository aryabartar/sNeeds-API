import requests
import json


class APIException(Exception):
    pass


class HTTPException(Exception):
    pass


class SkyroomAPI(object):
    def __init__(self, apikey):
        self.host = 'www.skyroom.online'
        self.apikey = apikey
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }

    def __repr__(self):
        return "skyroom.SkyroomAPI({!r})".format(self.apikey)

    def __str__(self):
        return "skyroom.SkyroomAPI({!s})".format(self.apikey)

    def _request(self, action, params=None):
        url = 'https://' + self.host + '/skyroom/api/' + self.apikey
        data = {
            'action': action
        }
        if params:
            data['params'] = params
        try:
            content_data = requests.post(url, headers=self.headers, auth=None, json=data).content
            try:
                response = json.loads(content_data.decode("utf-8"))
                if (response['ok'] == True):
                    response = response['result']
                else:
                    raise APIException(
                        (u'APIException[error_code: %s]: %s' % (
                            response['error_code'], response['error_message'])).encode('utf-8')
                    )
            except ValueError as e:
                raise HTTPException(e)
            return response
        except requests.exceptions.RequestException as e:
            raise HTTPException(e)

    # 1.Service Management

    # to-be-implemented by Skyroom (hopefully) :)

    # 2.Rooms Management

    def getRooms(self, params=None):
        return self._request('getRooms', params)

    def countRooms(self, params=None):
        return self._request('countRooms', params)

    def getRoom(self, params=None):
        return self._request('getRoom', params)

    def getRoomUrl(self, params=None):
        return self._request('getRoomUrl', params)

    def createRoom(self, params=None):
        return self._request('createRoom', params)

    def updateRoom(self, params=None):
        return self._request('updateRoom', params)

    def deleteRoom(self, params=None):
        return self._request('deleteRoom', params)

    def getRoomUsers(self, params=None):
        return self._request('getRoomUsers', params)

    def addRoomUsers(self, params=None):
        return self._request('addRoomUsers', params)

    def removeRoomUsers(self, params=None):
        return self._request('removeRoomUsers', params)

    def updateRoomUser(self, params=None):
        return self._request('updateRoomUser', params)

    # 3. Users Management

    def getUsers(self, params=None):
        return self._request('getUsers', params)

    def countUsers(self, params=None):
        return self._request('countUsers', params)

    def getUser(self, params=None):
        return self._request('getUser', params)

    def createUser(self, params=None):
        return self._request('createUser', params)

    def updateUser(self, params=None):
        return self._request('updateUser', params)

    def deleteUser(self, params=None):
        return self._request('deleteUser', params)

    def getUserRooms(self, params=None):
        return self._request('getUserRooms', params)

    def addUserRooms(self, params=None):
        return self._request('addUserRooms', params)

    def removeUserRooms(self, params=None):
        return self._request('removeUserRooms', params)

    def getLoginUrl(self, params=None):
        return self._request('getLoginUrl', params)