import functools
from os import error
from flask import(
    Blueprint, flash, g, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET','POST'])
def register():
    db, c = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        position = request.form['position']
        error = None
        c.execute(
            'select id from user where username = %s', (username,)
        )
        
        if not username:
            error = 'Usuario es requerido'
        if not password:
            error = 'Contraseña requerida'
        if not position:
            error = 'Rol requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado'.format(username)

        if error is None:
            c.execute(
                'insert into user (username, password, position) values (%s, %s, %s)',
                (username, generate_password_hash(password), position)
            )
            db.commit()

            return redirect(url_for('auth.login'))
    
        flash(error)
    c.execute(
            'select * from rol'
        )
    roles = c.fetchall()
    return render_template('auth/register.html', roles=roles)

@bp.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida.'
        elif not check_password_hash(user['password'],password):
            error = 'Usuario y/o contraseña inválida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index.index'))

        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view 

@bp.route('logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))