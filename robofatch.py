import requests 
import urllib
import os

settings={'file':'robots.txt', 'url':'mheducation.com', 'pre':'www.', 'websep':'/', 'http':'http://'}
path_list=[]
removed_list=[]
dfile = settings['file']
found_list=[]
nonexist=[]

def cleanup(x):
    if os.path.exists(x):
        os.remove(x)

def path_loader(dfile):
    loader = open( dfile, "r" )
    remove1 ='Disallow:'
    remove2 = 'User-agent:'
    remove3 = 'Sitemap'
    remove4 = 'Allow'
    remove5 = 'User-Agent: *'
    remove6 = 'User-agent: Mediapartners-Google'
    remove7 = 'User-agent: Googlebot-Image'
    remove8 = '#'
    remove9 = 'Crawl-delay:'

    #Cleaning the list
    for line in loader:
        if line == remove2:
            new_line = line.replace(remove2,'')
            path_list.append(new_line.strip())
        elif line.startswith( remove3 ):
            removed_list.append(line.strip())
        elif line.startswith( remove2 ):
            removed_list.append(line.strip())
        elif line.startswith( remove4 ):
            removed_list.append(line.strip())
        elif line.startswith( remove5 ):
            removed_list.append(line.strip())
        elif line.startswith( remove6 ):
            removed_list.append(line.strip())
        elif line.startswith( remove7 ):
            removed_list.append(line.strip())
        elif line.startswith( remove8 ):
            removed_list.append(line.strip())
        elif line.startswith( remove9 ):
            removed_list.append(line.strip())
        else:
            new_line = line.replace(remove1,'')
            path_list.append(new_line.strip())
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
    req = requests.get(URL)
    print "fetching:", URL
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
