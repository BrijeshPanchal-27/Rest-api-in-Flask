from flask import Flask,jsonify,session ,request
from flask_mysqldb import MySQL
import mysql.connector
from flask import Flask

app = Flask(__name__)


app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'brijssql'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'college'
mysql = MySQL(app)



@app.route('/createsuperuser', methods = ['POST'])
def create_superuser():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not password:
      return jsonify({'user , password and email are required'}),400
  
    is_superuser = data.get('is_superuser',False)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO authentication(username,email, password, active) VALUES( %s,%s,%s,%s )",
                  (username,email,password,1 if is_superuser else 0))


    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message':'superuser created successfully'}),201
  
  
    
@app.route('/login',methods = ['POST'])
def login():
    data=request.json
    login_identifier = data.get('login_identifier')
    password=data.get('password')
    
    if not login_identifier or not password :
        return jsonify({'error:login_identifier and passsword are required'}),400
    
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT * FROM authentication WHERE (username = %s or email = %s )and password= %s",
                  (login_identifier , login_identifier, password))
    user_data = cur.fetchone()
    mysql.connection.commit()
    cur.close()
      
    if not user_data:
       return jsonify({'error':'Incorrct username or email or password'}),401
    
    session ['username']= user_data[0]
    return jsonify({'message':'login successfully'}),200


@app.route('/changepassword',methods = ['POST'])

def change_password():
    data = request.json
    print(data)
    username = data.get('username')
    
    new_password = data.get('new_password')
    
    if not username or not new_password :
        return jsonify({'error : username and new password are required'}),400
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE authentication SET password = %s WHERE username = %s",(new_password,username))
    
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'password changed successfuly'}),200


@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('username',None)
    return jsonify({'message ' : 'logout successful'}),200


required_fields = ['person_id','person_name','person_email','person_password']

if __name__=='__main__':
    app.run(debug=True,port=8860)
