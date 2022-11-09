import os
from flask import render_template, request, redirect, flash
from app import app, db
from app.models import *
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

# ================== PRODUCT Hoang ============================
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

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
        # xu ly file
        image = request.files["img_name"]
        if image.filename == "":
            flash('Please Upload Image file', "danger")
            return redirect(request.url)
        if allowed_image(image.filename) and (not name or description):
            filename = secure_filename(image.filename)
            try:
                entry = PRODUCT(Name = name, Description = description, ImageUrl = filename, Status=1, Surcharge=0)
                db.session.add(entry)
                db.session.commit()
                image.save(app.config["IMAGE_UPLOADS"] +'\\'+ filename)
                flash('File upload Successfully !', "success")
                return redirect('/productmanage')
            except IntegrityError as e:
                flash('Something went wrong please try again later', "danger")
                return redirect(request.url)        
    return "Something went wrong"

@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "Something went wrong"

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            form = request.form
            name = form.get('name')
            description = form.get('description')
            entry.Name = name
            entry.Description = description
            db.session.commit()
        return redirect('/productmanage')

    return "Something went wrong"



@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/productmanage')

    return "Something went wrong"

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
    list_product = PRODUCT.query.all()
    return render_template('index.html', list_product = list_product)




@app.route('/productdetail/<int:product_id>')
def productdetail(product_id):
    product = PRODUCT.query.get(product_id)  
    return render_template('productdetail.html', product = product)

if __name__ == '__main__':
   
    print('test')
    
