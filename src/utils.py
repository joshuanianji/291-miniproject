def get_valid_int(prompt):
    '''
    Get a valid integer from the user
    '''
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def get_char_exact_len(prompt, length):
    '''
    Get a character from the user, but only if the length is exactly `length` long
    '''
    while True:
        user_input = input(prompt)
        if len(user_input) != length:
            print("Please enter exactly {} characters.".format(length))
            continue
        return user_input
