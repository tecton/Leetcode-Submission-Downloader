import requests

URL = 'https://leetcode.com/accounts/login/'

s = requests.Session()
s.get(URL)
csrftoken = s.cookies['csrftoken']

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': URL
}
           
def getSubmission(username, password):
    payload = {'csrfmiddlewaretoken': csrftoken,
               'login': username,
               'password': password}
    s.post(URL, data=payload, headers=headers)
    return s
