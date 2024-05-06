from flask import Flask, render_template, request, flash, redirect
##from tensorflow.keras.models import load_model
import sqlite3
import pickle
import numpy as np
import random
import requests
import warnings
warnings.filterwarnings('ignore')
model = pickle.load(open('LL.pkl', 'rb'))
import telepot
bot=telepot.Bot("5967745874:AAGjydD1YYZiNycgWMrXOJgue2SNoXG9ZoQ")
chatid="5286343673"
# bot1=telepot.Bot("6219379409:AAEp6-mjx71mG-HMjRLRJAcWk07-0djuTJQ")
# chatid1=""

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/class1')
def class1():
   return render_template('class1.html')

@app.route('/class2')
def class2():
   return render_template('class2.html')
@app.route('/class3')
def class3():
   return render_template('class3.html')
@app.route('/class4')
def class4():
   return render_template('class4.html')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry , Incorrect Credentials Provided,  Try Again')
        else:
           
            return render_template('logged.html')  #,bp=bp

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route("/kidneyPage")
def kidneyPage():
    return render_template('logged.html')


@app.route("/predictPage", methods = ['POST', 'GET'])
def predictPage():
    
 
    name = request.form['name']
    Age = request.form['age']
    sex = request.form['sex']
    if sex==1:
        sex="MALE"
    else:
        sex="FEMALE"
    bp = request.form['bp']
    oxy = request.form['oxy']
    print(oxy)
    hb = request.form['heart']
    ecg = request.form['ecg']
    Temperature = request.form['Temperature']
    to_predict_list = np.array([[float(bp),float(oxy),float(hb),float(ecg),float(Temperature)]])
    print(to_predict_list)
    prediction = model.predict(to_predict_list)
    output = prediction[0]
    print("Prediction is {}  :  ".format(output))
    print(output)
    
    # Check the output values and retrive the result with html tag based on the value
    
    if output == 1:
        result="Healthy    !" 
        med=""
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)))
        # bot1.sendMessage(chatid1,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)))
    if output == 2:
        result="Fever" 
        med="Diagnosis Drugs for Fever  \n  Paracetamol \n Acetaminophen \n Tylenol \n Aspirin \n  Acephen  \n Ecpirin \n"
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)))
        # bot1.sendMessage(chatid1,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)))
    if output == 3:
        result="Chest Pain" 
        med="Diagnosis Drugs for chest_pain \n Amlodipine \n Nadroparin \n Isosorbide \n Nifedipine \n Atenolol \n Diltiazem \n"
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)))
        # bot1.sendMessage(chatid1,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)))
    if output == 4:
        result="Critical" 
        med="You are critical \n consult the doctor immediately"
        print("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med))
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)))
        # bot1.sendMessage(chatid1,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)))
    
    
    # out=output
    print(result,output)
    return render_template('predict.html', result = result,out=output,name =name,med=med )  #,out=out

    # return render_template('logged.html')

@app.route('/msg',methods = ['POST', 'GET'])
def msg():
    if request.method == 'POST':
        fileName=request.form['filename']
        img='dataset/'+fileName
        bot.sendPhoto(chatid, photo=open(img,'rb'))
        # bot1.sendPhoto(chatid1, photo=open(img,'rb'))

    return render_template('logged.html')


if __name__ == '__main__':
	app.run(debug = True, use_reloader=False)
