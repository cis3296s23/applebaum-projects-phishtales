import pickle
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import tldextract
import ipaddress
import re
from flask import Flask, render_template, request
import validators


app = Flask(__name__)


def load_model():
    with open('model.pkl', 'rb') as f:
        tree = pickle.load(f)
    return tree

def featureExtract(url):
    length = len(url)

    #Check for words commonly found in phishing domains
    sensitive_words = ['login', 'password', 'bank', 'account', 'credit', 'card', 'security', 'verification']
    sensitive = 0
    for word in sensitive_words:
        if word in url.lower():
            sensitive = 1

    #Count the number of subdomains
    subdomains = tldextract.extract(url).subdomain.split('.')
    sub = len(subdomains)

    #CHeck to see if an ip address is being used instead of a domain
    ip = 0
    try:
        ipaddress.ip_address(url)
        ip = 1
    except ValueError:
        ip = 0

    #Check to see if a shortening service is being used
    short = 0
    shortening_services = ['bit.ly', 'goo.gl', 'ow.ly', 'tinyurl.com']
    pattern = r'^https?://(?:www\.)?(' + '|'.join(shortening_services) + ')/[a-zA-Z0-9]+$'
    if re.match(pattern, url):
        short = 1

    features = [length, sensitive, sub, ip, short]
    return features
    

def validate_url(url):
    return validators.url(url) 
    
def check_phishing(url):
    tree = load_model()
    features = np.array(featureExtract(url))
    y_pred = tree.predict(features.reshape(1, -1))[0]
    return y_pred == 1

@app.route('/', methods=['GET', 'POST'])  # method accept GET AND POST requests
def index():
    result = None
    if request.method == 'POST':   # when user submit the url
        url = request.form['url']    # store the url in url variable
        if url and validate_url(url):    # if url is valid and not empty
            is_safe = check_phishing(url)    # check if it is safe or phising
            result = 'safe' if is_safe else 'phishing'   
        else:
            result = 'invalid'
    return render_template('index.html', result=result)  # return the result in html file

if __name__ == '__main__':
    app.run(debug=True)
