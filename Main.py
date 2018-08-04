import login.py

def main():

    username = input('enter your username: ')
    password = input('enter your password: ')
    session = requests.session()
    handshake_mainPage = try_login(session, username,password)
    print(handshake_mainPage)
    session.close()

if __name__ == '__main__':
    main()
