import pickle
import numpy as np
import tldextract
import re
import sys

#Load pre-trained model from pickle
def load_model():
    with open('model.pkl', 'rb') as file:
        tree = pickle.load(file)
    return tree

# Feature 1: Presence of IP Address in URL
def usesIP(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)
    if match:
        return 1
    else:
        return 0


#Feature 2: Records URL length as an integer
def url_length(url):
    length = len(url)
    return length


#Feature 3: Checks for the presence of redirection in a URL with the sequence '//' after https or http
def redirect(url):
    if url[8:].find('//') >= 0:
        return 1
    else:
        return 0


#Feature 4: Checks for the uses of common shortening services which may be used to hide a URLs full contents
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


#Feature 5: Presence of Sensitive Words which are commonly associated with phishing scams
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


#Feature 6: Returns the number of subdomains including the top-level-domain.
def count_subdomains(url):
    subdomains = tldextract.extract(url).subdomain.split('.')
    return len(subdomains)

#Feature 7: Check for the presence of https in a URL.
def https(url):
    if url[:5] == "https":
        return 1
    else:
        return 0

#Feature 8: Check for the presence of http in a URL.
def http(url):
    if url[:4] == "http" and url[:5] != 'https' :
        return 1
    else:
        return 0

#Extracts features from a URL. Also adds features to record the count of the characters '!', '@', '#', '%', '&', '+', '-', '=', '.', '/', '\', and '?'
def feature_extraction(url):
    features = []
    symbols = ['!', '@', '#', '%', '&', '+', '-', '=', '.', '/', '\\', '?']
    #URL-based features
    features.append(usesIP(url))
    features.append(url_length(url))
    features.append(redirect(url))
    features.append(isShort(url))
    features.append(check_sensitive_words(url))
    features.append(count_subdomains(url))
    #Features 9-21
    for symbol in symbols:
        features.append(url.count(symbol))
    features.append(https(url))
    features.append(http(url))
    
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

#Main function used to generate a prediction.
def main():
    tree = load_model()
    url = takeInput()
    features = np.array(feature_extraction(url))
    y_pred = tree.predict(features.reshape(1, -1))[0]
    if y_pred == 0:
        print('{} is most likely not a phishing scam.'.format(url))
    else:
        print('{} is most likely a phishing scam.'.format(url))

if __name__ == '__main__':
    main()






