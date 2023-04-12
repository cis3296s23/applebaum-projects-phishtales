#!/usr/bin/env python
# coding: utf-8

# # Feature Engineering
# ### Create combined dataframe with phishing and legitimate URLs

# In[34]:


#Phishing URLs
import pandas as pd

phishing = pd.read_csv('phishing.csv')
phish = phishing.sample(n=10000, replace=False)
phish.shape


# In[35]:


#Select 75,000 legitimate URLs to be used (will shrink down once offline URLs are removed)
legitimate = pd.read_csv('legitimate.csv')
legit = legitimate.sample(n=10000, replace=False)
legit.shape


# In[36]:


#Add https:// to legit URL if not already present
legit["url"] = legit["url"].apply(lambda x: "https://" + x if not x.startswith("https://") and not x.startswith("http://") else x)
legit.head()


# In[37]:


#Combine dataframe and shuffle data
df = pd.concat([phish, legit], ignore_index=True).sample(frac=1).reset_index(drop=True)
df.shape


# ## URL-Based Features
#      Features are extracted from the URL itself.
#      Features include: 
#         1. Presence of IP Address in the URL
#         2. Presence of '@' in the URL
#         3. URL Length
#         4. The presence of redirection in the URL
#         5. Use of URL Shortening Services
#         6. The presence of sensitive words
#         7. Number of subdomains
#         8. Having a hyphen '-' in the domain name

# 
# ### Feature 1: Presence of IP Address in URL
# #### This is common in phishing scams

# In[38]:


import ipaddress
from urllib.parse import urlparse
def usesIP(url):
    try:
        ip = ipaddress.ip_address(url)
        return 1
    except:
        return 0


# ### Feature 2: Presence of '@' Symbol in URL
# #### The '@' symbol ignores all text proceeding it and is common in phishing scams

# In[39]:


def hasAt(url):
    if '@' in url:
        return 1
    else:
        return 0


# ### Feature 3: URL Length
# #### Longer URLs tend to be associated with phishing scams

# In[40]:


def url_length(url):
    length = len(url)
    return length


# ### Feature 4: Redirection
# #### The presence of '//' in a URL means that redirection is present. This is common in phishing scams
# #### Checks after the 8th index to ensure that https or http is not caught

# In[41]:


import re
def redirect(url):
    if url[8:].find('//') >= 0:
        return 1
    else:
        return 0


# ### Feature 5: URL Shortening
# #### Check for the presence of common URL shortening links which cause a redirection and are common in scams

# In[42]:


def isShort(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
    
    if re.search(shortening_services,url):
        return 1
    else:
        return 0


# ### Feature 6: Presence of Sensitive Words
# #### Phishing URLs commonly have sensitive words such as those listed below to trick unsuspecting users

# In[43]:


def check_sensitive_words(url):
    sensitive_words = r"Password|Account|Login|Verify|Security|Update|Payment|Card|Bank|Alert|Access|" \
                            r"Confirm|Information|Identity|Social Security|Verification|Fraud|Suspended|Limited|" \
                            r"Urgent|Unusual|Unauthorised|Suspicious|Lock|Reset|Expired|Invalid|Disabled|Termination|" \
                            r"Deactivation|Hack|Breach|Compromised|Phishing|Scam|Fake|Spam|Spoof|Spoofing|Impersonation|" \
                            r"Emergency|Critical|Failure|Error|Warning|Alert|Threat|Danger|Attack|Virus"
    if re.search(sensitive_words, url, flags=re.IGNORECASE):
        return 1
    else:
        return 0


# ### Feature 7: Number of Subdomains
# #### Phishing scams commonly have a higher number of subdomains

# In[44]:


import tldextract
def count_subdomains(url):
    subdomains = tldextract.extract(url).subdomain.split('.')
    return len(subdomains)


# ### Feature 8: Presence of '-' in Domain
# #### This is common in phishing scams to appear to be a legitimate common website

# In[45]:


import urllib
def isHyphen(url):
    if '-' in urlparse(url).netloc:
        return 1            
    else:
        return 0   


# ## HTML and Javascript-Based Features
#      Features are extracted from the domain.
#      Features include: 
#         1. IFrame redirection
#         2. Status bar customization
#         3. Disabling right-click
#         4. Number of redirects

# ### Feature 9: HTML Redirection
# #### Check for IFrame tags which is HTML redirection commonly present in phishing scams

# In[46]:


import re
import requests
def htmlredir(response):
    if response == "":
        return 0
    if re.findall(r"[|]", response.text):
        return 1
    else:
        return 0


# ### Feature 10: Status Bar Customization
# #### Status bar customization commonly can hide the URL of hyperlinks and is associated with phishing

# In[47]:


from bs4 import BeautifulSoup
def check_status_bar(response):
    if response == "":
        return 0
    soup = BeautifulSoup(response.content, 'html.parser')
    anchors = soup.find_all('a')
    for anchor in anchors:
        if anchor.get('title') != None and len(anchor.get('title')) > 0:
            return 1
    return 0


# ### Feature 11: Disabling Right-Click
# #### Another common phishing feature

# In[48]:


def rightClick(response):
  if response == "":
    return 0
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 1
    else:
      return 0


# ### Feature 12: Number of Redirects
# #### Phishing links commonly contain a higher number of redirects in their HTML

# In[49]:


def forwarding(response):
  if response == "":
    return 0
  else:
    if len(response.history) <= 2:
      return 1
    else:
      return 0


# # Create new DataFrame based off of features

# In[ ]:


from urllib.parse import urlparse
def feature_extraction(url, label):
    features = []
    #URL-based features
    features.append(usesIP(urlparse(url).hostname))
    features.append(hasAt(url))
    features.append(url_length(url))
    features.append(redirect(url))
    features.append(isShort(url))
    features.append(check_sensitive_words(url))
    features.append(count_subdomains(url))
    features.append(isHyphen(url))

    #HTML and Javascript-based features
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(htmlredir(response))
    features.append(check_status_bar(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
    
    features.append(label)
    
    return features


# In[ ]:


#Extract features for all entries
final_features = []
for i in range(0, 20000):
    url = df['url'][i]
    label = df['label'][i]
    final_features.append(feature_extraction(url,label))


# In[ ]:


#Create featurized dataframe
feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                      'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
                      'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards', 'Label']

data = pd.DataFrame(final_features, columns= feature_names)


# In[ ]:


#Store data as a csv
data.to_csv('data.csv', index=False)

