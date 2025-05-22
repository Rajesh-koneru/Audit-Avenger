from flask_login import current_user
from flask import session ,redirect

def only_one(*role):
    def decorator(func):
        def checker(*arg):
            if not current_user.is_authenticated:
                print(f'i am here.....{current_user["username"]} ')
                return redirect('/signup_page')
            if len(role)==2:
                if  session['username'] !=role[0] and session['username'] !=role[1]:
                    print(f'or i am here ... you are {session["username"]} not {role}')
                    print('access denied')
                    return redirect('/signup_page')
            elif len(role)==1:
                if session['username']!='Admin@raghu':
                    print(f'your are not admin ,you are {session["username"]}')
                    return redirect('/signup_page')
            return func(*arg)
        return checker
    return decorator

