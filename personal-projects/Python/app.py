import os
from flask import Flask,redirect,url_for,render_template,request
from werkzeug.utils import secure_filename     
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail



app = Flask(__name__)
db = SQLAlchemy(app)

# ENV = 'dev'

# if ENV == 'dev':
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:prostgres@localhost:5432/feedback'
app.debug = False
app.config['SQLAlchemy_DATABASE_URI'] = ''
        
app.config['SQLALCHEMY_TRACK_MODIFICATIONS,'] = False
        
        
        
    

        
        
class Feedback(db.Model):
        __tablename__ = 'feedback'
        id = db.Column(db.Integer, primary_key=True)
        customer = db.Column(db.String(200), unique=True)
        restaurant = db.Column(db.String(200))
        rating = db.Column(db.Integer)
        comments = db.Column(db.Text())
        
        def __init__(self, customer, restaurant, rating, comments):
                self.customer = customer
                self.restaurant = restaurant
                self.rating = rating 
                self.comments = comments
                

@app.route("/") 
def uploader():        
        path = 'static/uploads/' 
        uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))        # Sorting as per image upload date and time
        print(uploads)
        #uploads = os.listdir('static/uploads')
        uploads = ['uploads/' + file for file in uploads]
        uploads.reverse()
        return render_template("home.html",uploads=uploads)            # Pass filenames to front end for display in 'uploads' variable

app.config['UPLOAD_PATH'] = 'static/uploads'             # Storage path    
@app.route("/upload",methods=['GET','POST'])
def upload_file():                                       # This method is used to upload files 
        if request.method == 'POST':
                f = request.files['file']
                print(f.filename)
                #f.save(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                return redirect("/")           # Redirect to route '/' for displaying images on fromt end
        
@app.route('/form', methods=['GET'])
def form():
        return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
        if request.method == 'POST':
               customer = request.form['customer']
               restaurant = request.form['restaurant']
               rating = request.form['rating']
               comments = request.form['comments']
               #print(customer, restaurant, rating, comments)
        if customer == '' or restaurant == '':
                return render_template('form.html', message='Please enter required fields')
        
        
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:      
                data = Feedback(customer, restaurant, rating, comments)        
        db.session.add(data)  
        db.session.commit()
        send_mail(customer, restaurant, rating, comments)
        
        
        
        
        
        
        return render_template('success.html')
#     return render_template('form.html', message='You have already submitted feedback')
           
               
if __name__=="__main__":
        app.debug = True
        app.run()