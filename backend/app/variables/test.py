def change_email():
    global email
    email = email + '.com'

def main_func():
    global name
    name = 'harr'
    global email
    email = 'harr@email'
    change_email()
    print('1'+name)
    print('2'+email)

main_func()