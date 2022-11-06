from flask import render_template, request, redirect
from app import app, db
from app.models import *

jedi = "of the jedi"

# ================== PRODUCT Hoang ============================
@app.route('/productmanage')
def productmanage():
    entries = PRODUCT.query.all()
    return render_template('productmanage.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        description = form.get('description')
        if not name or description:
            entry = PRODUCT(Name = name, Description = description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/productmanage')

    return "of the jedi"

@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            form = request.form
            title = form.get('name')
            description = form.get('description')
            entry.title = title
            entry.description = description
            db.session.commit()
        return redirect('/')

    return "of the jedi"



@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/productmanage')

    return "of the jedi"

# @app.route('/turn/<int:id>')
# def turn(id):
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         if entry:
#             entry.status = not entry.status
#             db.session.commit()
#         return redirect('/')

#     return "of the jedi"
# ================================= END PRODUCT HOANG ======================================

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/productdetail/<product_id>')
def productdetail(product_id):
    return render_template('productdetail.html')

    
