from os import error
import app
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.auth import login_required
from app.db import get_db
from jinja2  import TemplateNotFound
import calendar


bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
        # Detecta la pagina actual
        # segment = get_segment( request )
        # Serve the file (if exists) from app/templates/FILE.html
    db, c = get_db()
    c.execute(
        'SELECT o.nombreOrigen, SUM(cuelgas) as SumaCuelgas FROM colgados c'
        ' inner join origenes o on c.origen=o.idOrigen'
        ' group by origen'
    )
    cuelgas_origenes = c.fetchall()
    labels= []
    values= []
    for cuelga_origen in cuelgas_origenes:
        values.append(int(cuelga_origen['SumaCuelgas']))
        labels.append(cuelga_origen['nombreOrigen'])

    c.execute(
        'select SUM(kgsCosechado) as TotalCosechado, camada from cosechas'
        ' group by camada'
    )
    camada_cosechado = c.fetchall()
    l= []
    v= []
    for cosechado in camada_cosechado:
        v.append(int(cosechado['TotalCosechado']))
        l.append(cosechado['camada'])
        
    return render_template('index.html', labels=labels, values=values, l=l, v=v)
    

    # except TemplateNotFound:
    #     return render_template('page-404.html'), 404



# Helper - Extrae el nombre de la pagina actual mediante el request
# def get_segment( request ): 

#     try:

#         segment = request.path.split('/')[-1]

#         if segment == '':
#             segment = 'index'

#         return segment    

#     except:
#         return None  