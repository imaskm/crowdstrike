'''
Created on Jan 6, 2019

@author: ashwani
'''

from bs4 import BeautifulSoup as SOUP

import requests as HTTP
import os
import git

def get_data():
    url = "https://s3-ap-southeast-1.amazonaws.com/he-public-data/crowdstriked6215ff.html"

    response = HTTP.get(url)
    data = response.text

    soup = SOUP(data, "html")

    data = soup.find_all("tr",recursive=True)
    return data

def get_repos():

    data = get_data()

    branches=[None]*2
    for i in range(1,len(data)):
        text= str(data[i] ) 
        #print(text)
        s = text.find("<td>")
        #print(s)
        e = text.find("</td>",s+4)
    
        branches[i-1]= [text[s+4:e]]
    
        s = text.find("<td>",e+1)
        e = text.find("</td>",s+4)
    
        branches[i-1].append(text[s+4:e])
    
        s = text.find("<td>",e+1)
        e = text.find("</td>",s+4)
    
        branches[i-1].append(text[s+4:e])
    return branches

repos = get_repos()

for repo in repos:
    print(repo)
    try:
        path= os.getcwd()
        path+="/"
        path+=repo[0]
        #os.makedirs(path, 0755, exist_ok=False)
        #os.mkdir(path,0755)
        if not os.path.exists(path):
            print("path-------",path)
            os.mkdir(path)
        else:
            os.system("rm -rf %s" % path)
            os.mkdir(path)
        
        cloned = git.Repo.clone_from(repo[1],path, None, None)
        os.chdir(repo[0])
        os.system("ls -a")
        os.system("git branch -r")
        os.system('git checkout -b %s' % repo[2] )
        os.system("git status")
        url =  "https://s3-ap-southeast-1.amazonaws.com/he-public-data/index837f27d.js"
        new_file_data = HTTP.get(url).text
        file = open("new_file.py", "w+") 
        file.write(new_file_data)
        
        #os.system("touch new_file.py")
        print("new file created")
        os.system("git add new_file.py")
        os.system("git status")
        os.system("git config --global user.name ashwani")
        os.system("git config --global user.email ashwanisharma686@gmail.com")
        os.system("git commit -m 'new file added'")
        os.system("git remote show origin")
        #os.system("git remote set-url origin git+ssh://git@github.com/username/reponame.git")
        os.system("git push origin %s" % repo[2] )
        os.chdir("../")
    except :
        print("Error occurred while processing")
    
