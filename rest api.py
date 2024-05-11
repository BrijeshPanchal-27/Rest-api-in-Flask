
    
from flask import Flask,jsonify,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Device(db.Model):
    __tablename__ = 'devices_ma'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(255), nullable=False)
    device_name = db.Column(db.String(255), nullable=False)
    device_type = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    port = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean, default=True)


def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/api',methods = ['POST'])
def add_device():
    try:
        data = request.json
        required_fields = ['device_id','device_name','device_type','url',' ip','port']
       
       
        for field in required_fields:
            
            if field not in data or not data[field]:
                
                return jsonify({'error 'f'missing or empty value for {field}'}),400
            
            
            
            existing_device =  Device.query.filter_by(device_id=data['device_id']).first()
            if existing_device:
                return jsonify({'error' : 'device id already exsist'}),400
            active = data.get('active',True)
            
            new_device = Device(
                device_id=data['device_id'],
                device_name=data['device_name'],
                device_type=data['device_type'],
                url=data['url'],
                ip=data['ip'],
                port=data['port'],
                active=active
            )
            
            db.session.add(new_device)
            db.session.commit()
            
        
            return jsonify({'message':'successfully added device data'}),201
            
    except Exception as e:
        return jsonify ({'error': str(e)}),400
    

    
@app.route('/api/devices/<int:device_id>',methods = ['PATCH'])



def update_device (device_id):
    
    try:
        device = Device.query.get(device_id)
        if not device : 
            return jsonify({'error'': device not found'}),400
    
        data = request.json
    
        if 'device_id' in data:
            device.device_id = data['device_id']
        if 'device_name' in data:
            device.device_name = data['device_name']
        if 'device_type' in data:
            device.device_tyoe = data['device_type']
        if 'url' in data:
            device.url = data['url']
        if 'ip' in data:
            device.ip = data['ip']
        if 'port' in data:
            device.port = data['port']
        if 'active' in data:
            device.active = data['active']
        
        db.session.commit()
    
        return jsonify({'message':'device info updated successfully'}),200
                                        
    except Exception as e :
        return jsonify ({'error':str(e)}),400



  
@app.route('/check_device',methods = ['GET'])
def get_all_devices():
    
    try:
        devices = Device.query.all()
        device_list = []
        for device in devices:
            device_data = {
                'id': device.id,
                'device_id': device.device_id,
                'device_name':device.device_name,
                'device_type':device.device_type,
                'url':device.url,
                'ip':device.ip,
                'port':device.port,
                'active':device.active 
            }
            
            
            device_list.append(device_data)
            print(device_data)
            
        response=jsonify({'devices':device_list})
        response.headers.add("Access-Control-Allow-Origin","*")
        return response
    
    except Exception as e :
        return jsonify({'error':str(e)}),500
    
    
@app.route('/api/delete/<int:device_id>',methods = ['DELETE'])   
def delete(device_id):
    device = Device.query.get(device_id)
    db.session.delete(device)
    db.session.commit()
    return {"message": "device deleted."}

if __name__ == "__main__":
  app.run(debug=True,port=5002)
CORS(app,supports_credentials=True)
    
    
    
    
            
            
            
            
  
  
