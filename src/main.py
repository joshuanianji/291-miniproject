from pydoc import doc
import sqlite3
import time
from getpass import getpass
from datetime import datetime
import utils

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
        cid = utils.get_char_exact_len('ID (char 4): ', 4).upper()

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

    sid = int(datetime.now().strftime('%Y%m%d%H%M%S'))

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
    while True:
        mid = utils.get_valid_int('Movie ID (int): ')

        # Check if mid already exists
        cursor.execute('SELECT mid FROM movies WHERE mid = ?;', (mid,))
        if cursor.fetchone():
            print('Movie with mid {} already exists!'.format(mid))
        else:
            break
    title = input('Title: ')
    year = utils.get_valid_int('Year (int): ')
    runtime = utils.get_valid_int('Runtime (int): ')

    # Add movie
    cursor.execute('INSERT INTO movies (mid, title, year, runtime) VALUES (?, ?, ?, ?);', (mid, title, year, runtime))

    print('Entering cast members. At any time, press "q" to quit and finish adding cast members.')
    while True:
        pid = input('Cast member PID (char 4): ').upper()
        if pid == 'Q':
            print('Finishing adding cast members...')
            break
        elif len(pid) != 4:
            print('Invalid PID! please enter 4 characters')
            continue

        # look up member id 
        cursor.execute('SELECT * FROM moviePeople mp WHERE mp.pid = ?', (pid,))
        data = cursor.fetchone()

        # Cast member exists - add role
        if data:
            prompt = input('Confirm adding cast member {}, born in {}? (Y/N) '.format(data['name'], data['birthYear']))
            if prompt.upper() == 'Y':
                role = input('Role: ')
                cursor.execute('INSERT INTO casts (mid, pid, role) VALUES (?, ?, ?);', (mid, pid, role))
                connection.commit()
                print('Cast member {} added to {} with role {}!'.format(data['name'], title, role))
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

    print('Added movie {}!'.format(title))




def update_recommendations(user):
    '''
    The editor should be able to select a monthly, an annual or an all-time report and see a listing of movie pairs m1, m2 such that some of the customers who have watched m1, have also watched m2 within the chosen period. Any such pair should be listed with the number of customers who have watched them within the chosen period, ordered from the largest to the smallest number, and with an indicator if the pair is in the recommended list and the score. The editor should be able to select a pair and (1) add it to the recommended list (if not there already) or update its score, or (2) delete a pair from the recommended list.
    '''
    global connection, cursor
    
    choice =''
    while True:
        choice = input('Do you want to see a monthly (m), annual (a) or an all-time (at) report? ').lower()
        if choice == 'm' or choice == 'a' or choice == 'at':
            break
        else:
            print('Wrong input')


     #if score is 0 that means movie2 is not in recommended list of movie1
    query= ''' SELECT t1.m1, t1.m2, COUNT(DISTINCT t1.cid) as c, IFNULL(t2.score, 0)
    FROM
    (
    (
        SELECT w1.mid as m1, w2.mid as m2, strftime('%m', s1.sdate) as sdate, w1.cid as cid
        FROM sessions s1, watch w1, movies m1, sessions s2, watch w2, movies m2
        WHERE strftime('%m', s1.sdate) = strftime('%m', s2.sdate)
            AND s1.cid = s2.cid
            AND w1.sid = s1.sid
            AND w1.cid = s1.cid
            AND w2.sid = s2.sid
            AND w2.cid = s2.cid
            AND w1.mid !=  w2.mid
            AND w1.mid = m1.mid
            AND w2.mid = m2.mid
            ANd 2*w1.duration > m1.runtime
            AND 2*w2.duration > m2.runtime
    ) t1
    LEFT OUTER JOIN
    (
        SELECT r.watched as m1, r.recommended as recommend, r.score as score
        from recommendations r
    ) t2 
    ON (t1.m1 = t2.m1 AND t2.recommend = t1.m2)
    )
    GROUP BY t1.m1, t1.m2, strftime('%m', t1.sdate)
    ORDER BY c  DESC; '''


    qery2 = '''
     SELECT t1.m1, t1.m2, COUNT(DISTINCT t1.cid) as c, IFNULL(t2.score, 0)
 FROM
 (
 (
         SELECT w1.mid as m1, w2.mid as m2, strftime('%Y', s1.sdate) as sdate, w1.cid as cid
         FROM sessions s1, watch w1, movies m1, sessions s2, watch w2, movies m2
         WHERE strftime('%Y', s1.sdate) = strftime('%Y', s2.sdate)
             AND s1.cid = s2.cid
             AND w1.sid = s1.sid
             AND w1.cid = s1.cid
             AND w2.sid = s2.sid
             AND w2.cid = s2.cid
             AND w1.mid != w2.mid
             AND w1.mid = m1.mid
             AND w2.mid = m2.mid
             ANd 2*w1.duration >= m1.runtime
             AND 2*w2.duration >=m2.runtime
     ) t1
     LEFT OUTER JOIN
     (
        SELECT r.watched as m1, r.recommended as recommend, r.score as score
         from recommendations r
     ) t2 
     ON (t1.m1 = t2.m1 AND t2.recommend = t1.m2)
 )
 GROUP BY t1.m1, t1.m2, strftime('%Y', t1.sdate)
 ORDER BY c  DESC;
    '''

    #if score is 0 that means movie2 is not in recommended list of movie1
    allTimeQuery =  '''
   SELECT t1.m1, t1.m2, COUNT(DISTINCT t1.cid) as c, IFNULL(t2.score, 0)
 FROM
 (
 ( 
         SELECT w1.mid as m1, w2.mid as m2,  w1.cid as cid 
         FROM sessions s1, watch w1, movies m1, sessions s2, watch w2, movies m2
          WHERE  s1.cid = s2.cid
             AND w1.sid = s1.sid
             AND w1.cid = s1.cid
             AND w2.sid = s2.sid
             AND w2.cid = s2.cid
             AND w1.mid != w2.mid
             AND w1.mid = m1.mid
             AND w2.mid = m2.mid
             ANd 2*w1.duration >= m1.runtime
             AND 2*w2.duration >=m2.runtime
     ) t1
     LEFT OUTER JOIN
     (
        SELECT r.watched as m1, r.recommended as recommend, r.score as score
         from recommendations r
     ) t2 
     ON (t1.m1 = t2.m1 AND t2.recommend = t1.m2)
 )
 GROUP BY t1.m1, t1.m2
 ORDER BY c  DESC;'''

    query2 = '''
    SELECT * FROM sessions'''
    rows = ''
    if (choice == 'm'):
        k = 'm'
        rows = cursor.execute(query).fetchall()
    elif choice == 'a':
        k = 'Y'
        rows = cursor.execute(qery2).fetchall()
    else:
        rows = cursor.execute(allTimeQuery).fetchall()
    for row in rows:
        print(row[0], row[1], row[2], row[3])
    #Have to work on rest of the functionality for 
    



    


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
        db_path='./public.db'
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
