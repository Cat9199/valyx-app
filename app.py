import os
from flask import Flask, render_template, request, url_for, redirect,session,Response
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import base64
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQLAlchemy(app)
class products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    sizes = db.Column(db.String(80))
    price=db.Column(db.Integer)
    colors = db.Column(db.String(80))
    image=db.Column(db.LargeBinary)
    quantity=db.Column(db.Integer)
    pv= db.Column(db.String(80))
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    name = db.Column(db.String(120))
    password = db.Column(db.String(80))
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    email=db.Column(db.Integer)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    sizes = db.Column(db.String(80))
    price=db.Column(db.Integer)
    colors = db.Column(db.String(80))
    image=db.Column(db.LargeBinary)
    quantity=db.Column(db.Integer)
    pv= db.Column(db.String(80))
    
def main():
    print('i ame the fun')
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/card")
def card():
    my_p=Card.query.filter_by(email=session['email'])
    return render_template('card.html',info=my_p)
@app.route("/register")
def reg():
    try:
        user =session["email"] 
        if user:
            return render_template('base.html',mess='login')
    except :
            return render_template("register.html")
    return render_template('register.html')
@app.route("/shop-bags")
def shop_bags():
    list1=products.query.filter_by(pv='bags').all()
    return render_template('shop.html' ,products=list1,items='Bags')
@app.route("/shop-tshirts")
def shop_tshirts():
    list1=products.query.filter_by(pv='tshirts').all()
    return render_template('shop.html' ,products=list1,items='T-Shirts')
@app.route("/shop-hody")
def shop_hody():
    list1=products.query.filter_by(pv='hody').all()
    return render_template('shop.html' ,products=list1,items='Hody')
@app.route('/<int:t_id>/viwe/', methods=('GET', 'POST'))
def viwe(t_id):

    info=products.query.filter_by(id=t_id).first()
    lp=products.query.filter_by(pv=info.pv).all()
    return render_template('shop-single.html',info=info,lp=lp)
@app.route('/<int:t_id>/viwe/add', methods=('GET', 'POST'))
def adddd(t_id):
    info=products.query.filter_by(id=t_id).first()
    lp=products.query.filter_by(pv=info.pv).all()
    return render_template('shop-single.html',info=info,lp=lp,mess= 'add')
@app.route("/logout" ,methods=[ "POST"])
def logout():
    session['email']= None
    return redirect('/')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/login")
def LOGIN():
    try:
        user =session["email"] 
        if user:
            return render_template('base.html',mess='login')
    except :
            return render_template("login.html")
    return render_template('LOGIN.HTML')
@app.route("/log-m",methods=[ "POST"])
def log():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            # Login successful
            session["email"]=email
            return redirect(url_for('home'))
            session["pn"] = 0
        else:
            # Login failed
            return render_template('login.html', error='Invalid email or password')
        
@app.route("/sun-m",methods=[ "POST"])
def sunapp():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['password_confirmation']
    if password == cpassword :
        user=User(name=name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        session["email"]=email
        return redirect('/')
    else:
        return render_template('register.html', error='The password does not match')
    
# ...
@app.route("/admin")
def admin():
    if session['email']=='admin@gmail.com':
        return render_template('madmin.html')
    return "404"
@app.route("/<int:t_id>/addtocatd")
def addtocatd(t_id):
        return redirect('/')
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        print('ok')
        # Retrieve form data
        name = request.form['product-name']
        price = request.form['price']
        description = request.form['description']
        file = request.files['image']
        quantity = request.form['quantity']
        category= request.form.get('category')
        colors = " ".join(request.form.getlist('colors'))

        # Save product to database
        product = products(name=name, price=price,pv =category, description=description, colors=colors,image=file.read(), quantity=quantity)
        db.session.add(product)
        db.session.commit()
        image_data = base64.b64encode(product.image).decode('utf-8')
        return render_template('add_product.html',mess='Add product',pname=name,image_data=image_data)
    else:
        return render_template('add_product.html')
@app.route('/p/<int:img_id>/img_pic')
def img(img_id):
    img = products.query.get_or_404(img_id)
    return Response(img.image, mimetype='image/jpeg')
@app.route("/addtocard/<int:p_id>")
def addtocard(p_id):
    yt=products.query.get(p_id)
    new_item=Card(
        name=yt.name,
        pid=yt.id,
        email=session['email'],
        description=yt.description,
        sizes=yt.sizes,
        price=yt.price,
        colors=yt.colors,
        image=yt.image,
        quantity=yt.quantity,
        pv=yt.pv)
    db.session.add(new_item)
    db.session.commit()
    session["pn"] +=1
    print(session["pn"])
    return redirect(f'/{p_id}/viwe/add')
@app.route("/Checkout")
def Checkout():
    return render_template('Checkout.html')
if __name__ == '__main__':
        print('new user')
        app.run(port=200,debug=True)
        