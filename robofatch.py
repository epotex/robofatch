import requests 
import requests.exceptions
import urllib
import os

# User Agents

Google_Bot = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1',
    'From': '+http://www.google.com/bot.html'
}

settings={
          'file':'robots.txt',
          'url':'cnn.com',
          'pre':'www.',
          'websep':'/',
          'http':'http://', 
          'https':'https://',
          'usebot': "no"
          }

path_list=[]
removed_list=[]
dfile = settings['file']
found_list=[]
nonexist=[]


def roboclean():
    '''If the lines inside the robots.txt file start with item in the list, the script will remove this line'''
    cleaners=[ 
              'Crawl-delay:',
              '#',
              'User-agent: Googlebot-Image',
              'User-agent: Mediapartners-Google',
              'User-Agent: *',
              'User-agent:',
              'User-agent:',
              'Sitemap:'
              ]
    for clean in cleaners:
        yield clean


def cleanup(x):
    if os.path.exists(x):
        os.remove(x)

def path_loader(dfile):
    loader = open( dfile, "r" )
    trim1 ='Disallow:' 
    trim2 = 'Allow'
    #Cleaning the list
    for line in loader:
        if line.startswith(trim1) or line.startswith(trim2):
            new_line = line.replace(trim1,'') or line.replace(trim2,'')
            if new_line in path_list:
                pass
            else:
                path_list.append(new_line.strip())
            for x in roboclean():
                if line.startswith(x):
                    removed_list.append(line.strip())

    loader.close()
       
def robo_graber(proto,pre,baseurl,websep, file):

    URL = proto + pre + baseurl + websep + file
    settings['work_url'] = URL
    try:
        urllib.urlretrieve (URL, file)
    except requests.packages.urllib3.exceptions.LocationParseError:
        print "LocationParseError"
        pass
    
def url_graber(proto,pre,baseurl,  path):
    URL = proto + pre + baseurl +   path
    req = requests.get(URL, headers=Google_Bot )
    print "fetching:", URL
    try:
        if not req.ok:
            nonexist.append(path)
        else:
            found_list.append(URL)
    except requests.exceptions.SSLError:
        print "--- Switching to HTTPS"
        URL = settings['https'] + pre + baseurl +   path
        req = requests.get(URL ,  verify=False)

        if not req.ok:
            nonexist.append(path)
        else:
            found_list.append(URL)
    
print "--- New fatch for:" , settings['url'] 
print "--- fatching item:", settings['file']
print "#" *20  
print "--- preforming cleanup..."
cleanup(settings['file'])   
print "#" *20  
print "---grabbing the latest file from the server:", settings['file']
robo_graber(settings['http'],settings['pre'], settings['url'],settings['websep'], settings['file'])
print "#" *20  
print "---DONE!"
print "#" *20  
print "---processing the file"
path_loader(settings['file'])
print "#" *20
print "---Stripped lines:"
if not removed_list:
    print "No line stripped out"
else:    
    print "--- Those are the lines that have been stripped out from the file"
for item in removed_list:
    print "striped from robots.txt:", item
print "#" *20  
print "Working:"
print "#" *20
for item in path_list:
    url_graber(settings['http'],settings['pre'], settings['url'], item)
print "#" *20
print "---Found items"
print "#" *20
if not found_list:
    print "Found 0 results"    
else:
    for url in found_list:    
        print url
print "#" *20
print "---those item exist on the robots.txt file but returnd error while trying to fatch them:"    
print "#" *20
if not nonexist:
    print "Found 0 results"
else:    
    for url in nonexist:    
        print url
print "#" *20
print "Done!"
