#!/usr/bin/python
# -*- coding: utf-8 -*-

import leetcodeHTTPHelper
import re
import json
import os
import sys
import getpass

MAX_PAGE = 10000
ADD_FILE = 'add file: '
ALL_SUBMISSIONS_CHECKED = 'All submissions checked.'
CHECK_PAGE = 'Check page '
USAGE = "usage: leetcodeDownloader.py username"

SUBMISSION_URL = 'https://leetcode.com/api/submissions/my/'
BASE_URL = 'https://leetcode.com'

def downloadSubmission(session, name, file_type, URL):
    '''
    parse code from source and save it to file.
    '''
    filename = 'code/' + name + '.' + file_type
    if os.path.isfile(filename):
        return
    r = session.get(URL)
    code = re.search(r'submissionCode\:\ \'([^\']+)\'', r.content).group(1)
    code = code.encode('utf8')
    s = json.loads('{"code": "%s"}' % code)
    print ADD_FILE + filename
    f = open(filename, 'w')
    f.write(s['code'])
    f.close()


def checkSubmissions(username, password):
    s = leetcodeHTTPHelper.login(username, password)

    if not os.path.exists('code'):
        os.makedirs('code')

    for i in range(1, MAX_PAGE):
        print CHECK_PAGE + str(i)

        r = s.get(SUBMISSION_URL + str(i))
        trList = r.json()['submissions_dump']

        if(len(trList) == 0):
            print ALL_SUBMISSIONS_CHECKED
            break

        for tr in trList:
            result = tr['status_display']
            file_type = tr['lang']
            if (result == 'Accepted'):
                problemName = tr['title']
                codeUrl = BASE_URL + tr['url']
                downloadSubmission(s, problemName, file_type, codeUrl)


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print USAGE
    else:
        password = getpass.getpass()
        checkSubmissions(sys.argv[1], password)
