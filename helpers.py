from flask import render_template,session,redirect
from functools import wraps
from uuid import uuid4


def validate_inputs(dict):
    result = 'sucessfull'
    for key in dict:
        if not dict[key].strip():
            field = key.capitalize()
            result = f"{field} is empty"
            break
    return result


# render error page with message
def errored(message,code):
    return render_template('apology.html',message=message),code


def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# make a string ex: while uploading file
# we need to make sure each filename is unique so
# it does not ovverried another file
def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"


def admin_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if not session.get('admin'):
            return redirect('/admin')
        else:
            return f(*args,**kwargs)
    return wrapper
