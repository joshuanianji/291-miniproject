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

    keywords = input('Enter keywords: ').split()

    # Gets the count of the keyword in the movie titles
    QUERY = """
    SELECT titles.mid, titles.title, m.year, m.runtime, ifnull(counter_title, 0) + ifnull(counter_names, 0) + ifnull(counter_roles, 0) as count 
    FROM (
        SELECT mid, title, ((LENGTH(title) - LENGTH(REPLACE(lower(title), lower(:keyword), ''))) / LENGTH(:keyword)) 
        AS counter_title FROM movies
    ) titles LEFT OUTER JOIN (
        SELECT m.mid, m.title, SUM(query_counter) as counter_names
        FROM moviePeople mp 
            LEFT OUTER JOIN (SELECT pid, ((LENGTH(name) - LENGTH(REPLACE(lower(name), lower(:keyword), ''))) / LENGTH(:keyword)) as query_counter from moviePeople) mpCounts USING (pid)
            LEFT OUTER JOIN casts c USING (pid)
            LEFT OUTER JOIN movies m USING (mid)
        GROUP BY m.mid
        HAVING m.mid IS NOT NULL
    ) names USING (mid) LEFT OUTER JOIN (
        SELECT m.mid, m.title, SUM(query_counter) as counter_roles
        FROM casts c
            LEFT OUTER JOIN (SELECT pid, mid, ((LENGTH(role) - LENGTH(REPLACE(lower(role), lower(:keyword), ''))) / LENGTH(:keyword)) as query_counter from casts) castCounts ON (castCounts.pid = c.pid AND castCounts.mid = c.mid)
            LEFT OUTER JOIN moviePeople mp USING (pid)
            LEFT OUTER JOIN movies m USING (mid)
        GROUP BY m.mid
        HAVING m.mid IS NOT NULL
    ) roles USING (mid) LEFT OUTER JOIN movies m USING (mid)
    WHERE count > 0
    """

    results = {}

    # execute query for all keywords
    for keyword in keywords:
        cursor.execute(
            QUERY,
            {'keyword': keyword},
        )
        data = cursor.fetchall()
        for datum in data:
            # OHHH YEAH THIS CODE MAKES ME WANT TO CRY
            try:
                results[datum['mid']]['count'] += datum['count']
            except:
                results[datum['mid']] = {
                    'count': datum['count'],
                    'title': datum['title'],
                    'year': datum['year'],
                    'runtime': datum['runtime'],
                }
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['count'], reverse=True)

    if len(sorted_results) == 0:
        print('No results found')
        return

    i = 0 # keep track of where we are at the start of the list

    # using a for loop to make our "more" movies loop
    while True:
        for _ in range(0,5):
            elem = sorted_results[i][1]
            print('{}: {} ({}): {}min'.format(i + 1, elem['title'], elem['year'], elem['runtime']))
            i += 1
            if i >= len(sorted_results):
                break

        # Different output depending on if there are more than 5 movies we can show
        if i >= len(sorted_results):
            print('Please select a movie by its index:')
            user_input = utils.get_valid_input('> ', lambda x: x.isdigit() and int(x) > 0 and int(x) <= i)
        else:
            print('Please select a movie by its index or type "more":')
            user_input = input('> ').lower()

        if user_input == 'more' and i < len(sorted_results):
            # Show more results
            print('More results:')
            continue
        else:
            # User selected a movie
            n = int(user_input)
            selected_movie = sorted_results[n-1]
            print('Getting info for {} ({})'.format(selected_movie[1]['title'], selected_movie[1]['year']))

            # get all cast members of the movie
            QUERY = """
            SELECT name, role, mp.pid 
                FROM moviePeople mp
                LEFT OUTER JOIN casts c USING (pid)
                LEFT OUTER JOIN movies m USING (mid)
                WHERE m.mid = :mid
            """
            cursor.execute(
                QUERY,
                {'mid': selected_movie[0]},
            )
            cast_members = cursor.fetchall()
            print('Cast members:')
            for cast_member in cast_members:
                print('{} as {}'.format(cast_member['name'], cast_member['role']))
            
            if len(cast_members) == 0:
                print('No cast members found')
            
            # get the number of customers who have watched the movie (watched over 50% of it)
            QUERY = """
            SELECT COUNT(*) as count 
            FROM watch w, customers c, movies m
            WHERE w.cid = c.cid AND w.mid = m.mid AND m.mid = :mid AND w.duration*2 >= m.runtime
            """
            cursor.execute(
                QUERY,
                {'mid': selected_movie[0]},
            )
            watched_count = cursor.fetchone()['count']
            print('{} customer(s) have watched this movie'.format(watched_count))

            # Check if the user has a session
            cursor.execute(
                'SELECT * FROM sessions WHERE cid=:cid AND DURATION IS NULL', 
                {'cid': user }
            )
            session = cursor.fetchone()
            # Cast member follow or movie watch (note: there are 4 cases)
            if session is None:
                if len(cast_members) == 0:
                    # No cast memmbers, no session. Do nothing
                    print('Note: you do not have a session, so you can only select a cast member to follow. Since there are no cast members, we will return to the main menu')
                    break
                else:
                    # cast members, no session
                    print('Note: you do not have a session, so you can only select a cast member to follow. Select a cast member by its index:')
                    for i, x in enumerate(cast_members):
                        print('{}: {} as {}'.format(i + 1, x['name'], x['role']))

                    user_input = utils.get_valid_input('> ', lambda x: x.isdigit() and int(x) > 0 and int(x) <= len(cast_members))
                    print('Following {}!'.format(cast_members[int(user_input) - 1]['name']))
                    pid = cast_members[int(user_input) - 1]['pid']
                    follow_cast_member(user, pid)
                    break
            else:
                if len(cast_members) == 0:
                    # No cast members, session. Can only watch the movie
                    prompt = utils.get_in_list('Watch the movie? (y/n)', ['y', 'n'])
                    if prompt == 'y':
                        print('Watching {}!'.format(selected_movie[1]['title']))
                        mid = selected_movie[0]
                        start_movie(user, mid, session['sid'])
                    break
                else:
                    # with cast members, session
                    print('Type "1" to select a cast member and follow, and "2" to watch this movie')
                    prompt = utils.get_in_list('> ', ['1', '2'])
                    print('Received: {}'.format(prompt))
                    if prompt == '2':
                        print('Watching {}!'.format(selected_movie[1]['title']))
                        mid = selected_movie[0]
                        start_movie(user, mid, session['sid'])
                        break
                    else:
                        print('Select a cast member by the index:')
                        for i, x in enumerate(cast_members):
                            print('{}: {} as {}'.format(i + 1, x['name'], x['role']))

                        user_input = utils.get_valid_input('> ', lambda x: x.isdigit() and int(x) > 0 and int(x) <= len(cast_members))
                        print('Following {}!'.format(cast_members[int(user_input) - 1]['name']))
                        pid = cast_members[int(user_input) - 1]['pid']
                        follow_cast_member(user, pid)
                        break

    print('Returning to main menu...')




def start_movie(user, mid, sid):
    print('watching movie {}!'.format(mid))    
    pass


def follow_cast_member(cid, pid):
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


    query =  '''

     SELECT t1.m1, t1.m2, COUNT(DISTINCT t1.cid) as c, IFNULL(t2.score, 0)
 FROM
 (
 ( 
         SELECT w1.mid as m1, w2.mid as m2,  w1.cid as cid 
         FROM sessions s1, watch w1, movies m1, sessions s2, watch w2, movies m2
          WHERE  s1.cid = s2.cid
		    AND JULIANDAY('now') - JULIANDAY(s1.sdate) <= :time
			AND JULIANDAY('now') - JULIANDAY(s2.sdate) <= :time
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
 ORDER BY c  DESC; 
    '''

    rows = ''
    if (choice == 'm'):
        k = 'm'
        rows = cursor.execute(query, {'time': 30}).fetchall()
    elif choice == 'a':
        k = 'Y'
        rows = cursor.execute(query, {'time': 365}).fetchall()
    else:
        rows = cursor.execute(query, {'time': 2**10}).fetchall()
    
    if len(rows) < 1:
        print("Theres no report to show at this time.")
    else:
        for row in rows:
           # print(row[0], row[1], row[2], row[3])
            input_string = f"Press 'a' for adding the movie pair to recommended list, 'u' to update score and 'd' to delete the movie pair from recommended list \nWhat do you want to do with row where movie1 = {row[0]}, movie2 = {row[1]},\n and the number of customers who have watched it within the specified time period = {row[2]}"
            if row[3] == 0:
                input_string += f"and movie2 = {row[1]} is not in the recommended list of movie1({row[0]})"
            else:
                input_string += f"and movie2 ({row[1]})  is in the recommended list of movie1({row[0]}, with the score of {row[3]}"
            while True:
                Echoice = input(input_string).lower()
                if Echoice == 'a' or Echoice == 'd' or Echoice == 'u':
                    break
                print('Wrong Input\n')
            
            if Echoice == 'a':
                if row[3] != 0:
                    print('movie pair is already in recommended list\n')
                else:
                    while True:
                        try:
                            score = float(input('Whats the score you want to associate for this?'))
                            if score < 0 or nscore >=1:
                                raise ValueError('value needs to be between 0 and 1')
    
                        except ValueError as e:
                            print(e.args)
                        else:
                            break

                        

                    #Have to add a float check and a 0 < float <= 1 check
                    updateRecommQuery = '''
                    INSERT INTO recommendations VALUES(:m1, :m2, :score);
                    '''
                    cursor.execute(updateRecommQuery, {'m1': int(row[0]), 'm2': int(row[1]), 'score': score})
                    #, 
                    
            elif Echoice == 'd':
                if row[3] != 0:
                    delQuery = '''
                    DELETE FROM recommendations
                    WHERE watched = :m1 AND recommended = :m2;
                    '''
                    cursor.execute(delQuery, {'m1': int(row[0]), 'm2': int(row[1])})
            
            elif Echoice == 'u':
                if row[3] == 0:
                    print("Query couldn't be updated")
                else:
                    upQuery = '''
                    UPDATE recommendations
                    SET score = :sco
                    WHERE watched = :m1 AND recommended = :m2;
                    '''
                    newScore = float(input('Enter the desired new score\n'))
                    cursor.execute(upQuery, {'m1': int(row[0]), 'm2': int(row[1]), 'sco': newScore})



    connection.commit()

            


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
    with open("prj-tables.sql") as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)

    with open("public_data.sql") as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)

    # login page
    cid, cust = authenticate()
    
    #customerSessions('ABCD')
    # system page   
    system(cid, cust)

    return 0


if __name__ == "__main__":
    main()
    # db_path='./proj.db'
    # connect(db_path)

    # search_movie('bced')
