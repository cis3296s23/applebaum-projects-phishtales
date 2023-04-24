import pickle
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import tldextract
import ipaddress
import re
from urllib.parse import urlparse
import sys
import urllib
from flask import Flask, render_template, request

app = Flask(__name__)


#Load pre-trained model from pickle
def load_model():
    with open('model.pkl', 'rb') as f:
        tree = pickle.load(f)
    return tree

# Feature 1: Presence of IP Address in URL
def usesIP(url):
    try:
        ip = ipaddress.ip_address(url)
        return 1
    except:
        return 0


#Feature 2: Presence of '@' Symbol in URL
def hasAt(url):
    if '@' in url:
        return 1
    else:
        return 0


#Feature 3: URL Length
def url_length(url):
    length = len(url)
    return length


#Feature 4: Redirection
def redirect(url):
    if url[8:].find('//') >= 0:
        return 1
    else:
        return 0


#Feature 5: URL Shortening
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


#Feature 6: Presence of Sensitive Words
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


#Feature 7: Number of Subdomains
def count_subdomains(url):
    subdomains = tldextract.extract(url).subdomain.split('.')
    return len(subdomains)


#Feature 8: Presence of '-' in Domain
def isHyphen(url):
    if '-' in urlparse(url).netloc:
        return 1            
    else:
        return 0   

#Extract features
def feature_extraction(url):
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
    
    return features


#Take user input and check to see if it is formulated like a URL
def takeInput():
    url = input("Enter URL: ")
    #Contains no whitespace and at least one period
    regex = r"^[^\s]*\.[^\s]*$"
    if re.match(regex, url) is None:
        print('Invalid URL. Please try again.')
        sys.exit(1)
    else:
        if not url.startswith("https://") and not url.startswith("http://"):
            url = 'https://' + url
        return url
def check_phishing(url):
    tree = load_model()
    features = np.array(feature_extraction(url))
    y_pred = tree.predict(features.reshape(1, -1))[0]
    return y_pred == 0

@app.route('/', methods=['GET', 'POST'])  # method accept GET AND POST requests
def index():
    result = None
    if request.method == 'POST':   # when user submit the url
        url = request.form['url']    # store the url in url variable
        if url:  # if url is not empty
            if not url.startswith("https://") and not url.startswith("http://"):    # if url is valid and not empty
              url = 'https://' + url
            is_safe = check_phishing(url)    # check if it is safe or phising
            result = 'safe' if is_safe else 'phishing'   
        else:
            result = 'invalid'
    return render_template('index.html', result=result)  # return the result in html file

@app.route('/aboutProject')
def about_project():
    return render_template('aboutProject.html')

@app.route('/index')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)