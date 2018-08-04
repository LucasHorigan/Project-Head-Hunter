import requests
from bs4 import BeautifulSoup

def parse(soup):
    """
    function parses parsed soup text and returns randomly genreated SAML SSO url
    :param soup: Beautiful soup html parsed get request page text
    :return: randomly generated SAML SSO url
    """
    urls = []
    for line in soup: #iterarte through each line to find urls
        temp = ''
        marker = 0
        for char in line:
            temp += char
            marker +=1
            if char is'=' and line[marker] is '"' and line[marker+1] is 'h'\
                    and line[marker + 2] is 't' and line [marker+3] is 't':
                temp +=char
            else:
                continue
            urls.append(line) #if line contains url append to urls list
    SAML = ""
    for url in urls: #iterate through urls and obtain single line that contains SAML url
        if "SAML" in url:
            SAML = url
            break
    temp = ""
    marker = 0
    finalURL = ""
    for char in SAML: #iterate through each char and find where https starts
        temp +=char
        marker += 1
        endingQuoteMarker = 0
        if char is '=' and SAML[marker] is '"' and SAML[marker + 1] is 'h' \
                and SAML[marker + 2] is 't' and SAML[marker + 3] is 't':
                url = SAML[marker+1:] # url is equal from https://... to end of string
                for url_char in url:
                    endingQuoteMarker +=1
                    if url_char == '"':
                        finalURL = SAML[marker+1: (marker + endingQuoteMarker)] #add endingQuoteMarker and marker to get to end
                        break
    return finalURL


def try_login(session, username, password):
    """
    function tries to login jumping through a lot of hoops
    :param session: requests session to preserve cookies
    :param username: username entered by user
    :param password: password entered by user
    :return:
    """
    handshakeUrl = "https://rit.joinhandshake.com/login" #start url
    s = session.get(handshakeUrl) #start a session
    soup = BeautifulSoup(s.text, 'html.parser') #create soup to pass to parse method
    soup = str(soup).strip().splitlines()
    ssoURL = parse(soup) #grab SSO url
    session.get(ssoURL) #do a get request with sso url
    url = 'https://shibboleth.main.ad.rit.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1'
    session.get(url,params={
        'execution': 'e1s1'
    }) #execution is e1s1 as this is first session, first exection
    login_data = {'j_username': username,'j_password': password,'_eventId_proceed': ''} #dict of required queries for post request
    session.post(url, allow_redirects=True, data=login_data)
    final_url = 'https://app.joinhandshake.com/saml_consume' #final url since we don't have javascript
    mainPage = session.post(final_url, data={
        'method': 'post'
    })
    return mainPage
