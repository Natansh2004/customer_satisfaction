from flask import Flask, render_template, url_for, request
import joblib
import sqlite3

model = joblib.load('./models/logisticregre.lb')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/userdata')
def userdata():
    return render_template('project.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        flight_distance = int(request.form['flight_distance'])
        inflight_entertainment = int(request.form['inflight_entertainment'])
        baggage_handling = int(request.form['baggage_handling'])
        cleanliness = int(request.form['cleanliness'])
        departure_delay = int(request.form['departure_delay'])
        arrival_delay = int(request.form['arrival_delay'])

        gender = int(request.form['gender'])
        customer_type = int(request.form['customer_type'])
        travel_type = int(request.form['travel_type'])
        class_type = request.form['class_type']

        economy = 0
        economy_plus = 0
        if class_type == 'ECO':
            economy = 1
        elif class_type == 'ECO_PLUS':
            economy_plus = 1
        
        UNSEEN_DATA = [[age,flight_distance,inflight_entertainment,baggage_handling,\
                       cleanliness,departure_delay,arrival_delay,gender,\
                       customer_type,travel_type,economy,economy_plus]]

        # UNSEEN_DATA should be in double brackets
        # Because in training also x_train is 2D (double brackets)
        
        # order is important and also data type is also important
        # They should be same as x_train              

        PREDICTION = model.predict(UNSEEN_DATA)[0]
        # It will predict in 0 and 1
        # Model is trained in 0 and 1 

        label_dict = {0:'Dissatisfied',1:'Satisfied'}

        # INSERTING DATA INTO DATABASE

        conn = sqlite3.connect('cust_satisfaction.db')
        cur = conn.cursor()

        query_to_execute = """
        insert into cust_details values (?,?,?,?,?,?,?,?,?,?,?,?)
        """

        gender_dict = {1:'Male',0:'Female'}
        customer_type_dict = {1:'Disloyal',0:'Loyal'} 
        travel_type_dict = {1:'Personal',0:'Business'}

        data = [age,flight_distance,inflight_entertainment,baggage_handling,cleanliness,\
                departure_delay,arrival_delay,gender_dict[gender],customer_type_dict[customer_type],\
                travel_type_dict[travel_type],class_type,label_dict[PREDICTION]]
        
        cur.execute(query_to_execute,data)
        conn.commit()
        print('YOUR RECORD HAS BEEN STORED IN OUR DATABASE')
        cur.close()
        conn.close()
       
        #return label_dict[PREDICTION] 
        
        return render_template('output.html',output=label_dict[PREDICTION])        

if __name__ == '__main__':
    app.run(debug=True)
