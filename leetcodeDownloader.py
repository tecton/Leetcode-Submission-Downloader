#!/usr/bin/python
# -*- coding: utf-8 -*-

import leetcodeHTTPHelper
import re
import json
from bs4 import BeautifulSoup
import os
import sys
import getpass


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
    print 'add file: ' + filename
    f = open(filename, 'w')
    f.write(s['code'])
    f.close()


def checkSubmissions(username, password):
    SUBMISSION_URL = 'https://leetcode.com/submissions/'
    BASE_URL = 'https://leetcode.com'
    s = leetcodeHTTPHelper.getSubmission(username, password)
    if not os.path.exists('code'):
        os.makedirs('code')

    for i in range(1, 10000):
        print 'Check page ' + str(i)
        r = s.get(SUBMISSION_URL + str(i))
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            # delete '\n' between tr tags
            trList = filter(lambda a: a != '\n', list(soup.tbody.children))
        except:
            print 'All submissions checked.'
            break

        # structure of html tags are hard coded
        for tr in trList:
            tr = filter(lambda a: a != '\n', list(tr.children))
            submissionStatus = tr[2]
            try:
                result = submissionStatus.a.strong.contents[0]
                file_type = tr[4].contents[0]
                if (result == 'Accepted'):
                    problemName = tr[1].a.contents[0]
                    codeURL = BASE_URL + submissionStatus.a['href']
                    downloadSubmission(s, problemName, file_type, codeURL)
            except:
                pass


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print "usage: leetcodeDownloader.py username"
    else:
        password = getpass.getpass()
        checkSubmissions(sys.argv[1], password)
