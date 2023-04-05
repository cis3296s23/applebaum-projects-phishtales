import pickle
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import streamlit as st
import tldextract
import ipaddress
import re
import validators
import sys


#Load pre-trained model from pickle
def load_model():
    with open('model.pkl', 'rb') as f:
        tree = pickle.load(f)
    return tree

#Extract the features from a URL
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

#Take user input and check to see if it is formulated like a URL
def takeInput():
    url = input("Enter URL: ")
    #Contains no whitespace and at least one period
    regex = r"^[^\s]*\.[^\s]*$"
    if re.match(regex, url) is None:
        print('Invalid URL. Please try again.')
        sys.exit(1)
    else:
        return url

#Main function used for the program
def main():
    tree = load_model()
    url = takeInput()
    features = np.array(featureExtract(url))
    y_pred = tree.predict(features.reshape(1, -1))[0]
    if y_pred == 1:
        print('{} is most likely not a phishing scam.'.format(url))
    else:
        print('{} is most likely a phishing scam.'.format(url))

if __name__ == '__main__':
    main()






