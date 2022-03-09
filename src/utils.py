def get_valid_input(prompt, is_valid, error_msg='Please enter a valid input.'):
    '''
    Takes in a prompt and a predicate, and returns the first valid input from the user
    '''
    while True:
        user_input = input(prompt).lower()
        if is_valid(user_input):
            return user_input.strip()
        print(error_msg)

def get_valid_int(prompt):
    '''
    Get a valid integer from the user
    '''
    return get_valid_input(prompt, lambda x: x.isdigit(), 'Please enter a valid integer.')


def get_char_exact_len(prompt, length):
    '''
    Get a character from the user, but only if the length is exactly `length` long
    '''
    return get_valid_input(prompt, lambda x: len(x) == length, 'Please enter an input of length {}'.format(length))

def get_in_list(prompt, L):
    '''
    Gets a valid input from the user that is in the list L
    '''
    return get_valid_input(prompt, lambda x: x in list(map(lambda x: x.lower(), L)), 'Please enter a valid input (one of: {})'.format(', '.join(L)))

