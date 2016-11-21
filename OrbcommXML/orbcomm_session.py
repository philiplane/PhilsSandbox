import urllib2
from xml.etree import ElementTree

username = 'Polestar'
password = 'wrmhyvdy'
host = 'https://ipgwy.orbcomm.net/'


def get_session_id():

    auth_command = 'Authenticate?LOGIN=' + username + '&PSSWD=' + password
    auth_request = host + auth_command

    try:
        response = urllib2.urlopen(auth_request).read().decode("utf-8")
        # print(response)
        tree = ElementTree.fromstring(response)
        # for child in tree:
        #    print (child.tag, child.attrib)
        # print(tree.find('SESSION_ID').tag, ":", tree.find('SESSION_ID').text)
        # print(tree.find('RESULT').tag, ":", tree.find('RESULT').text)
        # print(tree.find('EXTEND_DESC').tag, ":", tree.find('EXTEND_DESC').text)
        return tree.find('SESSION_ID').text

    except urllib2.HTTPError as e:
            error = e.read().decode("utf-8")
            print(error)


def logout(session_id):

    logout_command = 'Logout?SESSION_ID=' + session_id
    logout_request = host + logout_command

    try:
        response = urllib2.urlopen(logout_request).read().decode("utf-8")
        print(response)
        tree = ElementTree.fromstring(response)
        return tree.find('RESULT').text

    except urllib2.HTTPError as e:
            error = e.read().decode("utf-8")
            print(error)


def main():
        session_id = get_session_id()
        print("session id:", session_id)
        print("logout result:", logout(session_id))

main()
