from functools import wraps
from flask import session, redirect


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			session['user_id']
			return f(*args, **kwargs)
		except KeyError:
			return redirect('/auth/login')

	return decorated_function


def no_login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			session['user_id']
			return redirect('/')
		except KeyError:
			return f(*args, **kwargs)

	return decorated_function
