from flask import Flask, request, jsonify
from CompressSchedule import CompressionFunction
# from Rough import CompressionFunction
from flask_cors import CORS
from pymongo import MongoClient

# First run the server before sending request to backend so that a local network could get created.

# Cross-Origin Resource Sharing (CORS) can be an issue when a client on a different domain or port (your React Native app) tries to access the backend. You might need to install and configure flask-cors in your Flask app to allow requests from your React Native client.

app = Flask(__name__)
CORS(app)

# MongoDB configuration
client = MongoClient("mongodb+srv://archit_gupta_0019:My_Lord%3B7@rescheduler.kmyql.mongodb.net/")
db = client['Users-Information']  # Database name
LibrariansInfo = db['Librarians Info']  # Collection name
SchedulesCompletion = db['Schedules Completion']  # Collection name
StudentInfo = db['Students Info']
StudentsSchedules = db['Students Schedules']

# In the backend API case, ensure to have a 3rd device to share the same network in both PC and real device emulator and also ensure that Windows Firewall is closed.

@app.route("/", methods=["GET", "POST"])
def compress():
    try:
        if request.method == 'POST':
            data = request.json
            ImportedDataFrame = data.get('ImportedDataFrame')
            currentTime = data.get('currentTime')
            PriorSelections = data.get('PriorSelections')
            FixedSelections = data.get('FixedSelections')
            RemovingSelections = data.get('RemovingSelections')
            output = CompressionFunction(ImportedDataFrame, currentTime, PriorSelections, FixedSelections, RemovingSelections)
            return jsonify(output)
        else:
            return 'COME with a POST request rascal !!'
    except:
        return jsonify({"error": "An exception occured in compress route"}), 500
    
# Example: Insert data into MongoDB
@app.route('/addDistributor', methods=['POST'])
def add_Distributor():
    try:
        data = request.json  # Get the JSON data from request
        uniqueID = data.get('uniqueID')
        Name = data.get('Name')
        PhoneNumber = data.get('Phone Number')
        DateJoined = data.get('Date Joined')
        City = data.get('City')
        State = data.get('State')
        Country = data.get('Country')
        if data:
            LibrariansInfo.insert_one(data)  # Insert into MongoDB
            DistributorAsUser = {
                "uniqueID": uniqueID,
                "Name": Name,
                "Phone Number": PhoneNumber,
                "Date Joined": DateJoined,
                "Email ID": data.get('Email ID'),
                "Gender": "",
                "Streak": "",
                "Subscription Type": "Library",
                "Distribution Name": data.get('Distribution Name'),
                "Distribution ID": data.get('Distribution ID'),
                "Distribution Branch": data.get('Distribution Name'),
                "City": City,
                "State": State,
                "Country": Country,
                "Type of Account": "Distributor",
            }
            StudentInfo.insert_one(DistributorAsUser)
            StudentsSchedules.insert_one({
                "uniqueID": data["uniqueID"],
                "Name": data["Name"],
                "Phone Number": data["Phone Number"],
                "ScheduleArray": []
            })  # Insert into MongoDB
            SchedulesCompletion.insert_one({
                "uniqueID": data["uniqueID"],
                "Name": data["Name"],
                "Phone Number": data["Phone Number"],
                "Completion": []
            })
            return jsonify({"message": "Data added successfully!"}), 201
        return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in addDistributor route"}), 500

# Example: Fetch data from MongoDB
@app.route('/GetDistributorInfo', methods=['POST'])
def getDistributorInfo():
    try:
        uniqueID = request.json
        if uniqueID:
            DistributorExists = LibrariansInfo.find_one({ "uniqueID": uniqueID }, {"_id": 0})
            if DistributorExists:
                return jsonify(DistributorExists), 201
            else:
                return jsonify("Distributor Didn't Exist"), 201
        else:
            return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in getDistributorInfo route"}), 500

@app.route('/GetAllDistrubutionsInfo', methods=["GET"])
def getAllDistrubutionsInfo():
    try:
        allDistributors = []
        for distributor in LibrariansInfo.find({}, {"_id": 0, "Distribution Name": 1, "Local Address": 1, "City": 1}):
            allDistributors.append(distributor)
        return jsonify(allDistributors), 201
    except:
        return jsonify({"error": "An exception occurred in getAllDistrubutionsInfo route"}), 500

@app.route('/MatchNumber', methods=['POST'])
def match_number():
    try:
        userPhoneNumber = request.json
        if userPhoneNumber:
            userExists = StudentInfo.find_one({ "Phone Number": userPhoneNumber })
            if userExists:
                return jsonify("true"), 201
            else:
                return jsonify("false"), 201
        else:
            return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in match_number route"}), 500
    
@app.route('/AddStudent', methods=['POST'])
def add_student():
    try:
        data = request.json
        if data:
            StudentInfo.insert_one(data)  # Insert into MongoDB
            StudentsSchedules.insert_one({
                "uniqueID": data["uniqueID"],
                "Name": data["Name"],
                "Phone Number": data["Phone Number"],
                "ScheduleArray": []
            })  # Insert into MongoDB
            SchedulesCompletion.insert_one({
                "uniqueID": data["uniqueID"],
                "Name": data["Name"],
                "Phone Number": data["Phone Number"],
                "Completion": []
            })
            return jsonify({"message": "Student added successfully!"}), 201
        return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in add_student route"}), 500

@app.route('/GetStudentInfo', methods=['POST'])
def get_studentInfo():
    try:
        data = request.json
        if data:
            if data["Type"] == "Phone Number":
                studentData = StudentInfo.find_one({ "Phone Number": data["Value"] }, {"_id": 0})
            elif data["Type"] == "uniqueID":
                studentData = StudentInfo.find_one({ "uniqueID": data["Value"] }, {"_id": 0})
            if studentData:
                return jsonify(studentData), 201
            else:
                return jsonify({"error": "No student found!"}), 400
        else:
            return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in get_studentInfo route"}), 500

@app.route('/UpdateStudent', methods=['POST'])
def update_Student():
    try:
        data = request.json
        if data:
            if data["Type"] == "Phone Number":
                StudentInfo.update_one({ "Phone Number": data["Value"] },
                {
                    "$set": data["Updates"]
                })
                return jsonify({"Message": "Student Updated!"}), 201
            elif data["Type"] == "uniqueID":
                StudentInfo.update_one({ "uniqueID": data["Value"] },
                {
                    "$set": data["Updates"]
                })
                return jsonify({"Message": "Student Updated!"}), 201
        else:
            return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in update_Student route"}), 500

@app.route('/Testing', methods=['POST'])
def Testing():
    try:
        data = request.json
        if data:
            return jsonify({"Status": "Data Received!"}, {"Message": data}), 201
        else:
            return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in Testing route"}), 500
    
if __name__=='__main__':
    app.run()
    # app.run(debug=True, host='0.0.0.0')