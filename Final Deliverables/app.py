import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from flask import Flask,request,render_template,redirect,url_for
from cloudant.client import Cloudant

#Load the saved model
model = load_model(r"Updated-Xception-diabetic-retinopathy.h5")
app = Flask(__name__)

#Authenticate using an API key
client = Cloudant.iam('297de4bb-7794-416b-b73e-8b8c19764e4e-bluemix','i4tgxLMeZNhc5x_efsiDsrMdrcF-TwpojFO6ogD9_BwC',connect=True)

#Create a database using an initialized client
my_database = client.create_database('diabetic-retinopathy')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template("index.html")
@app.route('/register')
def register():
    return render_template('register.html')

#Configuring the registration page
@app.route('/afterreg',methods=['POST'])
def afterreg():
    if request.method == "POST":
        name = request.form.post("name")
        mail = request.form.get("mail")
        pswd = request.form.get("password")
        data = {
            'mail': mail,
            'name': name,
            'psw':  pswd
        }
        print(data)

        query = {'mail': {'$eq': data['mail']}}

        docs = my_database.get_query_result(query)
        print(docs)
        print(len(docs.all()))

        if len(docs.all()) == 0:
            url = my_database.create_document(data)
            return render_template('register.html',pred="Registered Successfully! Please Login using your credentials")
        else:
            return render_template('register.html', pred="Member Already Exists! Please Login using your credentials")
    else:
        return render_template('register.html')

#Configuring the login page
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    if request.method == "POST":
        user = request.form.get('mail')
        passw = request.form.get('password')
        print(user,passw)

        query = {'mail':{'eq':user}}
        docs = my_database.get_query_result(query)
        print(docs)
        print(len(docs.all()))

        if len(docs.all()) == 0:
            return render_template('login.html',pred="Wrong Username or Password given! ")
        else:
            if ((user==docs[0][0]['mail'] and passw==docs[0][0]['psw'])):
                return redirect(url_for('prediction'))
            else:
                print('Invalid user')
    else:
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        return render_template('logout.html')

    #Configuring prediction page
    @app.route('/result',methods=["GET","POST"])
    def res():
        if request.method == "POST":
            f = request.files['image']
            basepath = os.path.dirname(__file__)#getting the current path i.e where app.py is present
            #print("current path",basepath)
            filepath = os.path.join(basepath,'uploads',f.filename)#from anywhere in the system we can give image but we want that img
            # print("upload folder",filepath)
            f.save(filepath)

            img = image.load_img(filepath,target_size = (299,299))
            x = image.img_to_array(log)#onverting img to array
            x = np.expand_dims(x,axis=0) #Adding one more dimension
            #print(x)

            img_data = preprocess_input(x)
            prediction = np.argmax(model.predict(img_data),axis=1)

            index = ['No Diabetic Retinopathy','Mild Diabetic Retinopathy','Moderate Diabetic Retinopathy','Severe Diabetic Retinopathy','Proliferative Diabetic Retinopathy']
            result = str(index[prediction[0]])
            print(result)
            return render_template('prediction.html',prediction=result)
        else:
            return render_template("prediction.html")

        if __name__ == "__main__":
            app.run(debug=False)