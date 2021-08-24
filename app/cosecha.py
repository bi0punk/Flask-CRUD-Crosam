from os import error
import app
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.auth import login_required
from app.db import get_db



bp = Blueprint('cosecha',__name__, url_prefix='/cosecha')

@bp.route('/', methods = ['POST', 'GET'])
@login_required
def index():
    db, c = get_db()
    if request.method=='POST':
        fechaCosecha = request.form['fechaCosecha']
        codigoCentro = request.form['codigoCentro']
        nroGuia = request.form['nroGuia']
        folio = request.form['folio']
        linea_guia = request.form['linea_guia']
        camada = request.form['camada']
        nroCuelga = request.form['nroCuelga']
        metroRed = request.form['metroRed']
        maxiSaco = request.form['maxiSaco']
        kgsCosechado = request.form['kgsCosechado']
        condicion = request.form['condicion']
        servicio = request.form['sembradora']
        patente = request.form['patente']
        destino = request.form['destino']
        error = None
        c.execute(
            'select nroGuia, folio from cosechas where nroGuia = %s or folio = %s', (nroGuia, folio,)
        )
        if not nroGuia:
            error = 'Número de Guia es requerida'
        if not folio:
            error = 'Folio es requerido'
        elif c.fetchone() is not None:
            error = 'Registro ya se encuentra guardado'
        if error is None:
            c.execute(
                'insert into cosechas (fechaCosecha, codigoCentro, nroGuia, folio, linea_guia, camada, nroCuelga, metroRed, maxiSaco, kgsCosechado, condicion, servicio, patente, destino)'
                ' values (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)', (fechaCosecha, codigoCentro, nroGuia, folio, linea_guia, camada, nroCuelga, metroRed, maxiSaco, kgsCosechado, condicion, servicio, patente, destino)
            )
            db.commit()
            return redirect(url_for('cosecha.index'))
        flash(error)
    
    c.execute(
        'select cos.idCosecha, cos.fechaCosecha, cos.codigoCentro, cos.nroGuia, cos.folio, cos.linea_guia, cos.camada, cos.nroCuelga, cos.metroRed, cos.maxiSaco, cos.kgsCosechado, cos.condicion, semb.nombreSembradora, cos.patente, des.nombreDestino'
        ' from cosechas cos'
        ' inner join sembradoras semb on cos.servicio=semb.idSembradora'
        ' inner join destinos des on cos.destino=des.idDestino order by idCosecha DESC'
    )
    cosechas=c.fetchall()
    c.execute(
        'select * from sembradoras'
    )
    sembradoras=c.fetchall()
    c.execute(
        'select * from destinos'
    )
    destinos=c.fetchall()

    return render_template('cosecha/index.html', sembradoras=sembradoras, destinos=destinos, cosechas=cosechas)



def get_cosecha(id):
    db, c = get_db()
    c.execute(
        'select c.idCosecha, c.fechaCosecha, c.codigoCentro, c.nroGuia, c.folio, c.linea_guia, c.camada, c.nroCuelga, c.metroRed, c.maxiSaco, c.kgsCosechado, c.condicion, semb.nombreSembradora, c.patente, d.nombreDestino'
        ' from cosechas c inner join sembradoras semb on c.servicio=semb.idSembradora'
        ' inner join destinos d on c.destino=d.idDestino'
        ' where c.idCosecha=%s', (id,)
    )
    cosecha=c.fetchone()

    if cosecha is None:
        abort(404, "La cosecha de id={} no existe".format(id))
    return cosecha



@bp.route('/<int:id>/update', methods = ['GET', 'POST'])
@login_required
def update(id):
    db, c = get_db()
    cosecha = get_cosecha(id)
    if request.method == 'POST':
        fechaCosecha = request.form['fechaCosecha']
        codigoCentro = request.form['codigoCentro']
        nroGuia = request.form['nroGuia']
        folio = request.form['folio']
        linea_guia = request.form['linea_guia']
        camada = request.form['camada']
        nroCuelga = request.form['nroCuelga']
        metroRed = request.form['metroRed']
        maxiSaco = request.form['maxiSaco']
        kgsCosechado = request.form['kgsCosechado']
        condicion = request.form['condicion']
        servicio = request.form['sembradora']
        patente = request.form['patente']
        destino = request.form['destino']
        error = None
        if not codigoCentro:
            error = 'El codigo de Centro es requerido'
        if error is not None:
            flash(error)
        else:
            c.execute(
                'update cosechas set fechaCosecha=%s, codigoCentro=%s, nroGuia=%s, folio=%s, linea_guia=%s, camada=%s, nroCuelga=%s, metroRed=%s, maxiSaco=%s, kgsCosechado=%s, condicion=%s,'
                ' servicio=%s, patente=%s, destino=%s where idCosecha=%s',
                (fechaCosecha, codigoCentro, nroGuia, folio, linea_guia, camada, nroCuelga, metroRed, maxiSaco, kgsCosechado, condicion, servicio, patente, destino, id)      
            )
            db.commit()
            return redirect(url_for('cosecha.index'))
    c.execute(
        'select * from sembradoras'
    )
    sembradoras=c.fetchall()
    c.execute(
        'select * from destinos'
    )
    destinos=c.fetchall()

    return render_template('cosecha/update.html', cosecha=cosecha, sembradoras=sembradoras, destinos=destinos)


@bp.route('/<int:id>/delete', methods = ['GET', 'POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from cosechas where idCosecha=%s', (id,)
    )
    db.commit()

    return redirect(url_for('cosecha.index'))