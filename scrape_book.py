
# coding: utf-8

# # Web Scraping Basics w/Requests and Beautiful Soup

# This file explains the basic mechanisms for beginning Python learners to `scrape` the web. 
# 
# Requests and BeautifulSoup are very popular libraries used by many Python developers.
# 
# By the end of this notebook you might even have a collection of new literature to read more about Python with!
# 

# ### Import needed libraries

# In[93]:

import requests
from bs4 import BeautifulSoup
import os


# ### Assign variables to Variables 
# 
# These will be used later in the code. In the future, we may want to import these variables from a .yaml or .json file. Configurations should be imported or extracted from a parsable, human-friendly config file. When setting up complex systems, it's nice to have configuration files thoughtfully organized.

# *html_target* refers to First html tag you want to scrape data from. 
# 
# *tag* refers to the string information you want to grab from a tag in that html_target
# 
# *f_ext* is the filename extension you want to search for (scraping pdf files)
# 
# *dir_name* is the name of the path you want to store the files in
# 
# *url* is the base url you want to scrape.

# In[108]:

html_target = "a"
tag = "href"
f_ext = ".pdf"
dir_name = "Ghodsi_Ali"
url = 'https://www.cs.berkeley.edu/~alig/papers'


# In[95]:

### Request and Collect


# We instantiate a request object and call the `.get` method on it. `r` is our `HTTP 1.1` response. 
# 
# From here we have:
# 
# *    status
# *    encoding
# *    text of the body --- should type check this
# *    content of the body --- type binary
# 
# Once we have our `html` we are ready to scrape the site for useful `href` tags`
# 
# 

# In[96]:


r = requests.get(url)

status = r.status_code
encoding = r.encoding
html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')
anchor = soup(html_target)


# In[97]:

def make_dir(directory):
    """
    return: None
    Makes directory if does not already exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


# #### download_url(url, endpoint)
# 
# This function makes a new request each time it's called. It writes the binary content to file.
# This could be two functions. One to get the new request object/content. And the other to actually write that content to file. This modular design can be implemented by the reader if the reader is so inclined.

# In[106]:

def download_url(url, endpoint):
    """
    return: None
    downloads file, requires url in global or class scope.
    """
    url_addr = "{url}/{endpoint}".format(url=url, endpoint=endpoint)
    file_path = "{directory}/{endpoint}".format(directory=dir_name, endpoint=endpoint)
    
    r = requests.get(url_addr)
    content_file = r.content
    
    with open(file_path, 'wb') as f:
        print """Downloading From: {url}\nWriting to: {file_path}""".format(
                                                url=url_addr, 
                                                file_path=file_path
                                                                    )
        f.write(content_file)
    


# This is the script in action. Isolated like this, it looks very meager. It will be reconfigured as a series of method calls in the next iteration.
# 

# In[105]:

print """Status: {status}\nEncoding: {encoding}""".format(status=status, 
                                                    encoding=encoding)
print "Begin downloading"

make_dir(dir_name)
for a in anchor:
    endpoint = a[tag]
    if endpoint[-4:] == f_ext:
            download_url(url, endpoint)
            print "Finished Download -- {tag}".format(tag=endpoint)
    #print "miss: {tag}".format(tag=endpoint)
    
print "Finished Downloading"

