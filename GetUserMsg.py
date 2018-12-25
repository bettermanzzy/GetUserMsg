#encoding:utf-8
import argparse
import requests
import pandas as pd
import time
import sys
from tqdm import tqdm
from requests import get
import re
from requests.auth import HTTPBasicAuth

BEARER_TOKEN = 'fbfd6b48b8c47c0c15d7'
uname = 'bettermanzzy'

def start_requests(url):
    #print('getting', url)
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token 5b2e094c24989ae1f09b6f120f46819e8e82047c',
               'Content-Type': 'application/json',
               'Accept': 'application/json'
               }
    return requests.get(url,headers=headers)

def findEmailFromContributor(username, repo, contributor):
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token d1e20c381ba7dd8bc6627c319fde0bdf95830ac8',
               'Content-Type': 'application/json',
               'Accept': 'application/json'
               }
    response = get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor), auth=HTTPBasicAuth(uname, '')).text
    latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
    if latestCommit:
        latestCommit = latestCommit.group(1)
    else:
        latestCommit = 'dummy'
    #print(latestCommit)
    commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit), auth=HTTPBasicAuth(uname, '')).text
    commitStr = commitDetails.encode('utf8')
    email_list = re.findall(r'<(.*)>', commitStr)
    if len(email_list) >= 1:
        email = email_list[0]
    return email

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    #parse.add_argument('integer',type=int,help='display an integer')
    parse.add_argument('--g',help="get github api message",type=str)
    parse.add_argument('--sf',help="get sourceforge api message",type=str)

    args = parse.parse_args()

    if args.sf:
        print("sourceforge url",args.sf)
        url_name = args.sf
        try:
            project_name = url_name.split('sourceforge.net/projects/')[1]
            project_name = project_name.split('/')[0]
        except:
            print("input error")

        url = 'https://sourceforge.net/rest/p/'+project_name

        r = requests.get(url,params={
            'access_token': BEARER_TOKEN,
            'ticket_form.summary': 'Test ticket',
            'ticket_form.description': 'This is a test ticket',
            'ticket_form.labels': 'test',
            'ticket_form.custom_fields._my_num': '7'})
        if r.status_code == 200:
            print('Ticket created at: %s' % r.url)
        else:
            print('Error [%s]:\n%s' % (r.status_code, r.text))

        name = []
        username = []
        url = []
        for  developer in r.json()['developers']:
            name.append(developer['name'])
            username.append(developer['username'])
            url.append(developer['url'])

        print('developers name ', name)
        print('developers username', username)
        print('developers url', url)

        dict = {'name': name,'username': username,'userurl': url}
        writer = pd.ExcelWriter(project_name + '.xlsx')
        df = pd.DataFrame(dict)
        df.to_excel(writer, columns=['name', 'username', 'userurl'], index=False,encoding='utf-8', sheet_name='Sheet')
        writer.save()

    if args.g:
        print("github url",args.g)
        sys_url = args.g
        try:
            git_name = sys_url.split('github.com/')[1]
            xlsx_name_list = git_name.split('/')
        except:
            print("Your input is error,please try again")
            sys.exit(0)

        username = None
        xlsx_name = None
        if len(xlsx_name_list) >= 2:
            xlsx_name = xlsx_name_list[1]
            username = xlsx_name_list[0]
        else:
            print("Your input is error,please try again")
            sys.exit(0)

        url = 'https://api.github.com/repos/' + username + '/' + xlsx_name + '/' + 'contributors'
        get_url = start_requests(url)
        get_data = get_url.json()
        print('the numbers of contributors : ', len(get_data))
        print('Begin to count the message of contributors:')

        name_git = []
        id_git = []
        email_git = []
        location_git = []
        company_git = []
        project_git = []
        commits_git = []
        follower_git = []
        try:
            for data in tqdm(get_data, ncols=120):
                id = data['login']
                emails = []
                email = findEmailFromContributor(username, xlsx_name, id)
                emails.append(email)
                commits = data['contributions']
                msg_url = data['url']
                get_msg = start_requests(msg_url).json()
                name = get_msg['name']
                if name is None:
                    name = id
                company = get_msg['company']
                location = get_msg['location']
                email1 = get_msg['email']

                if email1 != email and email1 is not None:
                    emails.append(email1.encode('utf8'))
                project = get_msg['public_repos']
                follower = get_msg['followers']

                name_git.append(name)
                id_git.append(id)
                email_git.append(emails)
                location_git.append(location)
                company_git.append(company)
                commits_git.append(commits)
                project_git.append(project)
                follower_git.append(follower)
                time.sleep(0.01)
        except:
            print('Appear an error,please checkout your input is a github_repos_url! Correct input should like "https://github.com/lz4/lz4"')

        # write data to git_name.csv file
        dict = {'name': name_git, 'githubID': id_git, 'email': email_git, 'location': location_git, 'company': company_git, 'commits': commits_git, 'project': project_git, 'followers': follower_git}
        writer = pd.ExcelWriter(xlsx_name + '.xlsx')
        df = pd.DataFrame(dict)
        df.to_excel(writer,columns=['name', 'githubID', 'email', 'location', 'company', 'commits', 'project', 'followers'],index=False, encoding='utf-8',sheet_name='Sheet')
        writer.save()

