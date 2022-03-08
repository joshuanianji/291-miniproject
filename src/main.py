import sqlite3
import time
from getpass import getpass
from datetime import datetime

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')

    connection.commit()
    return





def login():
    '''
    Returns ID of a user, and whether the user is a customer or not

    Keeps prompting for user credentials until a valid user is found.
    '''
    global connection, cursor

    while True:
        print('Please enter your user credentials')
        user = input('Username: ').lower()
        pwd = getpass()
        
        cursor.execute('SELECT * FROM customers WHERE lower(cid) = ? AND pwd = ?;', (user, pwd))
        if cursor.fetchone():
            cust = True
            break
        else:
            cursor.execute('SELECT * FROM editors WHERE lower(eid) = ? AND pwd = ?;', (user, pwd))
            if cursor.fetchone():
                cust = False
                break
            else:
                print("Invalid Username or Password. Please try again!")

    return user, cust


def signup():
    '''
    Signs up a customer (their CID must be unique)

    Returns the ID of the customer
    '''
    global connection, cursor 
    print('Welcome to the Movies291 signup page! Please enter your credentials you wish to use')
    
    while True:
        cid = input('ID: ').upper()

        if len(cid) != 4:
            print('Please input an ID that is exactly 4 characters.')
            continue

        cursor.execute('SELECT * FROM customers WHERE lower(cid) = ?;', (cid,))
        if cursor.fetchone():
            print('ID already exists! Please try again!')
        else:
            break

    pwd = getpass()
    name = input('Name: ')

    # Add cid and pwd into customers table
    cursor.execute('INSERT INTO customers VALUES (?, ?, ?);', (cid, name, pwd))
    connection.commit()

    print('Signup successful! Redirecting you to System page...')
    return cid


def end_session(cid):
    # End the session. The user should be able to end the current session. The duration should be set
    #  in minutes to the time passed in minutes from the time the session started until the current time.
    #   If the customer has been watching any movies, those will end 
    # and the duration watched will be recorded. Again the duration watched cannot exceed the duration of the movie.

    
    
  

    # if len(curSessUser) > 1:
    #     SessTBClosed = input('')


    curSessMovies = '''
    SELECT mid FROM WATCH where sid = :sid AND :cid = cid AND duration < 

    '''

    






    connection.commit()



def system(user, cust):
    '''
    Main system page for customers and editors
    '''
    global connection, cursor

    display_name = 'Customer ' + user if cust else 'Editor ' + user
    print(f'Welcome to the system page, {display_name}! Type "h" for help')


    while True:
        user_input = input('> ').upper()
        if user_input == 'H':
            if cust:
                print('You can:')
                print('1. Start a session (SS)')
                print('2. Search for a movie (SM)')
                print('3. End watching a movie (EM)')
                print('4. End a session (ES)')
                print('5. Logout (LO)')
            else:
                print('You can:')
                print('1. Add a movie (AM)')
                print('2. Update Recommendation (UR)')
                print('3. Logout (LO)')
        
        elif user_input == 'SS' and cust:
            print('Starting session...')
            create_session(user)
        
        elif user_input == 'SM' and cust:
            print('Searching for movie...')
            search_movie(user)
        
        elif user_input == 'EM' and cust:
            end_movie(user)
            print('Ending movie...')
        
        elif user_input == 'ES' and cust:
            curSessUser = ''' SELECT sid FROM SESSIONS WHERE cid = :cid AND duration = NULL '''
            # cursor.execute(curSessUser, {'cid':cid})

            # if len(curSessUser) > 1:
                

            # end_session(user, curSessUser)
            print('Ending session...')
        
        elif user_input == 'AM' and not cust:
            add_movie()
            print('Adding movie...')
        
        elif user_input == 'UR' and not cust:
            update_recommendations(user)
            print('Updating recommendation...')
        
        elif user_input == 'LO':
            print('Logging out...')
            close_sessions(user)
            break
        
        else:
            print('Invalid input! Type "H" for help')

    return 


def search_movie(user):
    '''
    The customer should be able to provide one or more unique keywords, and the system should retrieve all movies that have any of those keywords 
    in title, cast member name or cast member role. 
    
    For each match, at least the title, the year, and the duration should be displayed, and the result should be ordered based on the number of 
    matching keywords with movies matching the largest number of keywords listed on top. 
    
    If there are more than 5 matching movies, at most 5 matches will be shown at a time, letting the user select a movie or see more matches. 
    
    The customer should be able to select a movie and see more information about the movie including the cast members and the number of customers 
    who have watched it (the definition of watch in this project is as discussed in Assignment 2). 
    
    On a movie screen, the customer should have the options (1) to select a cast member and follow it, and (2) to start watching the movie.
    '''
    
    global connection, cursor
    pass




def start_movie(user, mid, sid):
    
    pass





def end_movie(user, sid, mid):
    '''
    Closes the movie (mid:int) being wated by the user (user:str) in session (sid:int)
    '''
    global connection, cursor

    # Find all 

    pass





def create_session(cid):
    '''
    
    '''
    global connection, cursor

    sid = int(datetime.now().strftime('%Y%m%d')[2:])

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    duration = None

    cursor.execute('''
    INSERT INTO sessions (sid, cid, sdate, duration) VALUES (:sid, :cid, :sdate, :duration);
    ''', {'sid': sid, 'cid': cid, 'sdate':current_date, 'duration': duration})

    #commit to save the changes
    connection.commit()






def add_movie():
    '''
    The editor should be able to add a movie by providing a unique movie id, a title, a year, a runtime and a list of cast members and their roles. To add a cast member, the editor will enter the id of the cast member, and your system will look up the member and will display the name and the birth year. The editor can confirm and provide the cast member role or reject the cast member. If the cast member does not exist, the editor should be able to add the member by providing a unique id, a name and a birth year.
    '''
    global connection, cursor

    print('Please enter the movie information')
    mid = input('Movie ID: ').upper()
    title = input('Title: ')
    year = input('Year: ')
    runtime = input('Runtime: ')

    print('Entering cast members. At any time, press "q" to quit and finish adding cast members.')
    while True:
        pid = input('Cast member PID: ').upper()
        if pid == 'Q':
            print('Finishing adding cast members...')
            break
        
        # look up member id 
        cursor.execute('SELECT * FROM casts c, moviePeople mp WHERE c.mid=? AND c.pid = mp.pid', (mid,))
        data = cursor.fetchone()

        # Cast member exists - add role
        if data:
            prompt = input('Confirm adding cast member {}, born in {}? (Y/N) '.format(data['name'], data['birthYear']))
            if prompt.upper() == 'Y':
                role = input('Role: ')
                cursor.execute('INSERT INTO casts VALUES (?, ?, ?);', (mid, pid, role))
                connection.commit()
            else:
                print('Rejecting cast member...')
        else:
            # Cast member does not exist - add member
            prompt = input('Cast member not found, create a new cast member with pid {}? (Y/N) '.format(pid)).upper()
            if prompt == 'Y':
                name = input('Name: ')
                birthYear = input('Birth Year: ')
                cursor.execute('INSERT INTO moviePeople VALUES (?, ?, ?);', (pid, name, birthYear))
                connection.commit()
                print('Cast member {} with ID {} added! You can now add it to the movie.'.format(name, pid))
            else:
                print('Rejecting cast member...')

    print('')
        
        
            


def update_recommendations(user):
    pass

def close_sessions(user):
    '''
    Closes all the user's sessions on log out
    '''
    global connection, cursor
    
    pass








def authenticate():
    cid = None
    cust = True
    print('Welcome to the login page! Press "L" to login or "S" to signup')
    while True:
        user_input = input('Please enter your choice: ')
        if user_input.lower() == 'l':
            cid, cust = login()
            break
        elif user_input.lower() == 's':
            cid = signup()
            break
        else:
            print('Invalid input! Press "L" to login and "S" to signup')

    return cid, cust


# custom_path used for testing
def main(custom_path=None):
    global connection, cursor

    # uncomment once we have to present
    # db_path = input('Enter DB path: (e.g. ./prj-tables.db): ')
    if custom_path is None:
        db_path='./proj.db'
        connect(db_path)
    else:
        connect(custom_path)

    # open and execute tables.sql
    # ! we don't need this later on!
    # with open("prj-tables.sql") as sql_file:
    #     sql_as_string = sql_file.read()
    #     cursor.executescript(sql_as_string)

    # login page
    cid, cust = authenticate()
    
    #customerSessions('ABCD')
    # system page   
    system(cid, cust)

    return 0


if __name__ == "__main__":
    main()
