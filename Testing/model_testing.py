import pytest
import subprocess
from phish_tales_run import usesIP
from phish_tales_run import url_length
from phish_tales_run import redirect
from phish_tales_run import isShort
from phish_tales_run import check_sensitive_words
from phish_tales_run import count_subdomains
from phish_tales_run import https
from phish_tales_run import http
import phish_tales_run


#Test the usesIP() function
def test_usesIP():
    google = 'https://www.google.com'
    phish = '209.191.122.70'
    assert usesIP(google) == 0
    assert usesIP(phish) == 1

#Test the url_length() function
def test_url_length():
    #Length is 22
    google = 'https://www.google.com'
    #Length is 28
    phish = 'http://bbportaldocliente.com'
    assert url_length(google) == 22
    assert url_length(phish) == 28

#Test the redirect() function
def test_redirect():
    google = 'https://www.google.com'
    phish = 'https://wetgdsf.ourhobby.com//'
    assert redirect(google) == 0
    assert redirect(phish) == 1

#Test the isShort() function
def test_isShort():
    google = 'https://www.google.com'
    phish = 'https://tinyurl.com/ybeun8xt'
    assert isShort(google) == 0
    assert isShort(phish) == 1

#Test the check_sensitive_words() function
def test_check_sensitive_words():
    google = 'https://www.google.com'
    phish = 'https://stage.orivet.com/uploads/redirect.html?verify=stevengeolus9@hotmail.com-5672b61564748b5118e2-21018a6664a6a6d88892'
    assert check_sensitive_words(google) == 0
    assert check_sensitive_words(phish) == 1

#Test the count_subdomains() function
def test_count_subdomains():
    test = 'https://www.sub1.sub2.google.com'
    assert count_subdomains(test) == 2

#Test the https() function
def test_https():
    test1 = 'https://www.google.com'
    test2 = 'http://www.wikipedia.com'
    assert https(test1) == 1
    assert https(test2) == 0

#Test the http() function
def test_http():
    test1 = 'https://www.google.com'
    test2 = 'http://www.wikipedia.com'
    assert http(test1) == 0
    assert http(test2) == 1


#Test phish_tales_run() main function with a variety of different URLs
def test_phish_tales_run():
    valid = ['www.google.com', 'www.wikipedia.org/', 'www.stackoverflow.com/']
    phish = ['https://xdbopa.com/clients/app/cGuytF_UXDG/', 'https://50.188.109.208.host.secureserver.net/tracko98214040011/', 'http://banconacionalcostarica.atsnx.com/?i=1']
    for link in valid:
        p = subprocess.Popen(['python3', 'phish_tales_run.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        user_input = link
        output, _ = p.communicate(input=user_input.encode())
        assert output.decode() == 'Enter URL: {} is most likely not a phishing scam.\n'.format(link)
    for link in phish:
        p = subprocess.Popen(['python3', 'phish_tales_run.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        user_input = link
        output, _ = p.communicate(input=user_input.encode())
        assert output.decode() == 'Enter URL: {} is most likely a phishing scam.\n'.format(link)
