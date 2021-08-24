from functools import total_ordering
from os import error

import flask
import app
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.auth import login_required
from app.db import get_db



bp = Blueprint('colgado',__name__, url_prefix='/colgado')

@bp.route('/', methods = ['GET', 'POST'] )
@login_required
def index():
    db, c = get_db()
    if request.method == 'POST':
        linea = request.form['linea']
        sistema = request.form['sistema']
        cuelgas = request.form['cuelgas']
        fechaColgado = request.form['fechaColgado']
        origen = request.form['origen']
        error = None
        c.execute(
            'select idColgado from colgados where linea = %s', (linea,)
        )
        if not linea:
           error = 'Linea es requerida'
        
        elif c.fetchone() is not None:
            error = 'Linea {} ya se encuentra registrada'.format(linea)

        if error is None:
            c.execute(
                'insert into colgados (linea, sistema, cuelgas, fechaColgado, origen)'
                ' values (%s, %s, %s, %s, %s)',(linea, sistema, cuelgas, fechaColgado, origen)
            )
            db.commit()
            return redirect(url_for('colgado.index'))
        flash(error)
    c.execute(
        'select * from colgados c '
        'inner join origenes o on c.origen = o.idOrigen order by idColgado DESC '
    )
    colgados = c.fetchall()
    c.execute(
        'select * from origenes'
    )
    origenes=c.fetchall()
    

    return render_template('colgado/index.html', colgados=colgados, origenes=origenes)


def get_colgado(id):
    db, c = get_db()
    c.execute(
        'select c.idColgado, c.linea, c.sistema, c.cuelgas, c.fechaColgado, o.nombreOrigen'
        ' from colgados c inner join origenes o'
        ' on c.origen=o.idOrigen where c.idColgado=%s',(id,)
    )
    colgado = c.fetchone()

    if colgado is None:
        abort(404, "El colgado de id={} no existe".format(id))
    return colgado


@bp.route('/<int:id>/update', methods = ['GET', 'POST'])
@login_required
def update(id):
    db, c = get_db()
    colgado = get_colgado(id)
    if request.method == 'POST':
        linea = request.form['linea']
        sistema = request.form['sistema']
        cuelgas = request.form['cuelgas']
        fechaColgado = request.form['fechaColgado']
        origen = request.form['origen']
        error = None

        if not linea:
            error = 'La linea es requerida'
        if error is not None:
            flash(error)
        else:
            
            c.execute(
                'update colgados set linea = %s, sistema = %s, cuelgas = %s, fechaColgado = %s, origen = %s where idColgado = %s', (linea, sistema, cuelgas, fechaColgado, origen, id)
            )
            db.commit()
            return redirect(url_for('colgado.index'))
    
    c.execute(
        'select * from origenes'
    )
    origenes=c.fetchall()
    return render_template('colgado/update.html', colgado=colgado, origenes=origenes)


@bp.route('/<int:id>/delete', methods =['GET','POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from colgados where idColgado = %s', (id,)
    )
    db.commit()
    return redirect(url_for('colgado.index'))









