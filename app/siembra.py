import flask
from app import colgado
from os import error
import app
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.auth import login_required
from app.db import get_db



bp = Blueprint('siembra',__name__, url_prefix='/siembra')

@bp.route('/', methods= ['GET', 'POST'])
@login_required
def index():
    db, c = get_db()
    if request.method == 'POST':
        fechaSiembra = request.form['fechaSiembra']
        nroGuia = request.form['nroGuia']
        origen = request.form['origen']
        recepcion = request.form['recepcion']
        valorUnidad = request.form['valorUnidad']
        gastoSemilla = request.form['gastoSemilla']
        gastoFlete = request.form['gastoFlete']
        servicioFlete = request.form['servicioFlete']
        total = request.form['total']
        gastoServicio = request.form['gastoServicio']
        sembradora = request.form['sembradora']
        error = None
        c.execute(
            'select idSiembra from siembras where nroGuia = %s', (nroGuia,)
        )
        if gastoServicio=='':
            gastoServicio = 0
        if not nroGuia:
            error = 'Nro de Guía requerida'
        elif c.fetchone() is not None:
            error = 'El Nro. de Guía {} ya ha sido registrado'.format(nroGuia)
        if error is None:
            c.execute(
                'insert into siembras (fechaSiembra, nroGuia, origen, recepcion, valorUnidad, gastoSemilla, gastoFlete, servicioFlete, total, gastoServicio, sembradora)'
                ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (fechaSiembra, nroGuia, origen, recepcion, valorUnidad, gastoSemilla, gastoFlete, servicioFlete, total, gastoServicio, sembradora)
            )
            db.commit()
            return redirect(url_for('siembra.index'))
        flash(error)
    c.execute(
        'select * from siembras s '
        'inner join serviciosFletes sf on s.servicioFlete = sf.idServicioFlete'
        ' inner join origenes o on s.origen = o.idOrigen'
        ' inner join sembradoras semb on s.sembradora = semb.idSembradora'
    )
    siembras = c.fetchall()
    c.execute(
        'select * from origenes'
    )
    origenes=c.fetchall()
    c.execute(
        'select * from serviciosFletes'
    )
    serviciosFletes=c.fetchall()
    c.execute(
        'select * from sembradoras'
    )
    sembradoras=c.fetchall()
    return render_template('siembra/index.html', siembras=siembras, origenes=origenes, serviciosFletes=serviciosFletes, sembradoras=sembradoras)

def get_siembra(id):
    db, c = get_db()
    c.execute(
        'select s.idSiembra, s.fechaSiembra, s.nroGuia, o.nombreOrigen, s.recepcion, s.valorUnidad,' 
        ' s.gastoSemilla, s.gastoFlete, sf.nombreServicioFlete, s.total, s.gastoServicio, semb.nombreSembradora'
        ' from siembras s'
        ' inner join origenes o on s.origen=o.idOrigen'
        ' inner join serviciosfletes sf on s.servicioFlete=sf.idServicioFlete'
        ' inner join sembradoras semb on s.sembradora=semb.idSembradora'
        ' where s.idSiembra=%s',(id,)
    )
    siembra = c.fetchone()
    if siembra is None:
        abort(404, "La siembra de id={} no existe".format(id))
    return siembra

@bp.route('/<int:id>/update', methods = ['GET', 'POST'])
@login_required
def update(id):
    db, c = get_db()
    siembra =get_siembra(id)
    if request.method == 'POST':
        fechaSiembra= request.form['fechaSiembra']
        nroGuia = request.form['nroGuia']
        origen = request.form['origen']
        recepcion = request.form['recepcion']
        valorUnidad = request.form['valorUnidad']
        gastoSemilla = request.form['gastoSemilla']
        gastoFlete = request.form['gastoFlete']
        servicioFlete = request.form['sf']
        total = request.form['total']
        gastoServicio = request.form['gastoServicio']
        sembradora = request.form['sembradora']
        error = None

        if not nroGuia:
            error = 'Numero de Guía requerida'
        if error is not None:
            flash(error)
        else:
            c.execute(
                'update siembras set fechaSiembra = %s, nroGuia = %s, origen= %s, recepcion = %s,'
                ' valorUnidad = %s, gastoSemilla = %s, gastoFlete = %s, servicioFlete = %s, total = %s, gastoServicio = %s,'
                ' sembradora = %s where idSiembra = %s', (fechaSiembra, nroGuia, origen, recepcion, valorUnidad, gastoSemilla, gastoFlete, servicioFlete, total, gastoServicio, sembradora, id)
            )
            db.commit()
            return redirect(url_for('siembra.index'))
    c.execute(
        'select * from origenes'
    )
    origenes=c.fetchall()

    c.execute(
        'select * from serviciosFletes'
    )
    sf=c.fetchall()

    c.execute(
        'select * from sembradoras'
    )
    sembradoras=c.fetchall()

    return render_template('siembra/update.html', siembra=siembra, origenes=origenes, sf=sf, sembradoras=sembradoras)


@bp.route('/<int:id>/delete', methods = ['GET', 'POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from siembras where idSiembra = %s', (id,)
    )
    db.commit()
    return redirect(url_for('siembra.index'))