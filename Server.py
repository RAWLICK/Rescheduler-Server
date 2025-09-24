from flask import Flask, request, jsonify
from Rough import CompressionFunction
# from Rough import CompressionFunction
from flask_cors import CORS
from pymongo import MongoClient
import os
# from twilio.rest import Client
# from dotenv import load_dotenv

# First run the server before sending request to backend so that a local network could get created.

# Cross-Origin Resource Sharing (CORS) can be an issue when a client on a different domain or port (your React Native app) tries to access the backend. You might need to install and configure flask-cors in your Flask app to allow requests from your React Native client.

# load_dotenv()  # loads the .env file

app = Flask(__name__)
CORS(app)

# Twilio Configuration
# account_sid = os.getenv["TWILIO_ACCOUNT_SID"]
# auth_token = os.getenv["TWILIO_AUTH_TOKEN"]
# TwilioClient = Client(account_sid, auth_token) 

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
            print(f"Output: {output}")
            return jsonify(output)
        else:
            print("Come with a POST request rascal !!")
            return 'COME with a POST request rascal !!'
    except Exception as e:
        print(f"Error: {e}. This is the error in compress route")
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
            print(f"Distributor added successfully: {data}")
            return jsonify({"message": "Data added successfully!"}), 201
        else:
            print("No data found in addDistributor route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in addDistributor route")
        return jsonify({"error": "An exception occurred in addDistributor route"}), 500

# Example: Fetch data from MongoDB
@app.route('/GetDistributorInfo', methods=['POST'])
def getDistributorInfo():
    try:
        uniqueID = request.json
        if uniqueID:
            DistributorExists = LibrariansInfo.find_one({ "uniqueID": uniqueID }, {"_id": 0})
            if DistributorExists:
                print(f"Distributor found: {DistributorExists}")
                return jsonify(DistributorExists), 201
            else:
                print("Distributor didn't exist")
                return jsonify("Distributor Didn't Exist"), 201
        else:
            print("No data found in getDistributorInfo route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in GetDistributorInfo route")
        return jsonify({"error": "An exception occurred in getDistributorInfo route"}), 500

@app.route('/GetAllDistrubutionsInfo', methods=["GET"])
def getAllDistrubutionsInfo():
    try:
        allDistributors = []
        for distributor in LibrariansInfo.find({}, {"_id": 0, "Distribution Name": 1, "Local Address": 1, "City": 1}):
            allDistributors.append(distributor)
        print(f"Returned All Distributors list")    
        return jsonify(allDistributors), 201
    except Exception as e:
        print(f"Error: {e}. This is the error in GetAllDistrubutionsInfo route")
        return jsonify({"error": "An exception occurred in getAllDistrubutionsInfo route"}), 500

@app.route('/MatchNumber', methods=['POST'])
def match_number():
    try:
        userPhoneNumber = request.json
        if userPhoneNumber:
            userExists = StudentInfo.find_one({ "Phone Number": userPhoneNumber })
            if userExists:
                print(f"User found: {userExists}")
                return jsonify("true"), 201
            else:
                print("User didn't exist")
                return jsonify("false"), 201
        else:
            print("No data found in match_number route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in MatchNumber route")
        return jsonify({"error": "An exception occurred in match_number route"}), 500
    
@app.route('/MatchEmail', methods=['POST'])
def match_email():
    try:
        userEmail = request.json
        if userEmail:
            userExists = StudentInfo.find_one({ "Email ID": userEmail })
            if userExists:
                print(f"User found: {userExists}")
                return jsonify("true"), 201
            else:
                print("User didn't exist")
                return jsonify("false"), 201
        else:
            print("No data found in match_email route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in MatchEmail route")
        return jsonify({"error": "An exception occurred in match_email route"}), 500

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
                "Email ID": data["Email ID"],
                "ScheduleArray": []
            })  # Insert into MongoDB
            SchedulesCompletion.insert_one({
                "uniqueID": data["uniqueID"],
                "Name": data["Name"],
                "Phone Number": data["Phone Number"],
                "Email ID": data["Email ID"],
                "Completion": []
            })
            print(f"Student added successfully")
            return jsonify({"message": "Student added successfully!"}), 201
        else:
            print("No data found in add_student route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in AddStudent route")
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
            elif data["Type"] == "Email ID":
                studentData = StudentInfo.find_one({ "Email ID": data["Value"] }, {"_id": 0})
            if studentData:
                print(f"Student found: {studentData}")
                return jsonify(studentData), 201
            else:
                print("No student found")
                return jsonify({"error": "No student found!"}), 400
        else:
            print("No data found in get_studentInfo route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in GetStudentInfo route")
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
                print(f"Student updated successfully with: {data['Value']}")
                return jsonify({"Message": "Student Updated!"}), 201
            elif data["Type"] == "uniqueID":
                StudentInfo.update_one({ "uniqueID": data["Value"] },
                {
                    "$set": data["Updates"]
                })
                print(f"Student updated successfully with: {data['Value']}")
                return jsonify({"Message": "Student Updated!"}), 201
        else:
            print("No data found in update_Student route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in UpdateStudent route")
        return jsonify({"error": "An exception occurred in update_Student route"}), 500

@app.route('/IncrementRescheduleClick', methods=['POST'])
def increment_reschedule_click():
    try:
        data = request.json
        if data:
            result = StudentInfo.update_one(
                {"uniqueID": data["uniqueID"]},         # Match document by ID (or any condition)
                {"$inc": {"RescheduledTimes": 1}}   # Increment the 'RescheduledTimes' field by 1
            )

            if result.modified_count == 1:
                return {"status": "success", "message": "RescheduledTimes incremented"}
            else:
                return {"status": "error", "message": "No document updated"}
        else:
            return jsonify({"error": "No data found!"}), 400
    except:
        return jsonify({"error": "An exception occurred in IncrementRescheduleClick route"}), 500
    
@app.route('/GetAllStudents', methods=['POST'])
def get_all_students():
    try:
        data = request.json
        if data:
            allStudents = []
            for student in StudentInfo.find({ "Distribution ID": data["Distribution ID"] }, {"_id": 0}):
                required_fields = {
                    "uniqueID": student["uniqueID"],
                    "Student_Name": student["Name"],
                    "Phone_Number": student["Phone Number"],
                    "Branch": student["Distribution Branch"]
                }
                allStudents.append(required_fields)
            print(f"Returned All Students list for Distribution ID")
            return jsonify(allStudents), 201
        else:
            print("No data found in get_all_students route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in get_all_students route")
        return jsonify({"error": "An exception occurred in get_all_students route"}), 500
    
@app.route('/UpdateScheduleArray', methods=['POST'])
def update_ScheduleArray():
    try:
        data = request.json
        if data:
            if data["Process"] == "Add":
                StudentsSchedules.update_one(
                    { "uniqueID": data["uniqueID"] },
                    { "$push": { "ScheduleArray": data["SubjectInfoObject"] } }
                )
                print(f"SubjectInfoObject added successfully")
                return jsonify({"Message": "SubjectInfoObject Added!"}), 201
            elif data["Process"] == "Delete":
                StudentsSchedules.update_one(
                    { "uniqueID": data["uniqueID"] },
                    { "$pull": { "ScheduleArray": {"uniqueID": data["SubjectUniqueID"]} } }
                )
                print(f"SubjectInfoObject deleted successfully")
                return jsonify({"Message": "SubjectInfoObject Deleted!"}), 201
        else:
            print("No data found in update_ScheduleArray route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in update_ScheduleArray route")
        return jsonify({"error": "An exception occurred in update_ScheduleArray route"}), 500

@app.route('/GetScheduleArray', methods=['POST'])
def get_ScheduleArray():
    try:
        data = request.json
        if data:
            if data["Type"] == "Phone Number":
                scheduleData = StudentsSchedules.find_one({ "Phone Number": data["Value"] }, {"_id": 0, "ScheduleArray": 1})
            elif data["Type"] == "Email ID":
                scheduleData = StudentsSchedules.find_one({ "Email ID": data["Value"] }, {"_id": 0, "ScheduleArray": 1})
            if scheduleData:
                print(f"Sended the ScheduleArray")
                return jsonify(scheduleData["ScheduleArray"]), 201
            else:
                print("No schedule found")
                return jsonify({"error": "No schedule found!"}), 400
        else:
            print("No data found")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in get_ScheduleArray route")
        return jsonify({"error": "An exception occurred in get_ScheduleArray route"}), 500
    
@app.route('/UpdateExistingSubjectsArray', methods=['POST'])
def update_ExistingSubjectsArray():
    try:
        data = request.json
        if data:
            if data["Process"] == "Add":
                SchedulesCompletion.update_one(
                    { "uniqueID": data["uniqueID"] },
                    { "$push": { "Completion": data["StatsSubjectInfoObject"] } }
                )
                print(f"StatsSubjectInfoObject added successfully")
                return jsonify({"Message": "StatsSubjectInfoObject Added!"}), 201
            elif data["Process"] == "Delete":
                SchedulesCompletion.update_one(
                    { "uniqueID": data["uniqueID"] },
                    { "$pull": { "Completion": {"uniqueID": data["StatsSubjectUniqueID"]} } }
                )
                return jsonify({"Message": "StatsSubjectInfoObject Deleted!"}), 201
            elif data["Process"] == "UpdateSubject":
                SchedulesCompletion.update_one(
                    { "uniqueID": data["uniqueID"] },
                    { "$set": {
                        "Completion.$[comp].Subject": data["NewExistingSubject"]["Subject"],
                        "Completion.$[comp].Current_Duration": data["NewExistingSubject"]["Current_Duration"]
                    }},
                    array_filters=[{
                        "comp.uniqueID": data["NewExistingSubject"]["uniqueID"]
                    }]
                )
                print(f"StatsSubjectInfoObject updated successfully")
                return jsonify({"Message": "StatsSubjectInfoObject Updated!"}), 201
            elif data["Process"] == "AddCompletion":
                for i in data["PercentageArray"]:
                    SchedulesCompletion.update_one(
                        {"uniqueID": data["uniqueID"]},
                        {"$push": 
                            {
                                "Completion.$[comp].Dataframe": i["ProgressInfo"]
                            }
                        },
                        array_filters=[{
                            "comp.uniqueID": i["SubjectUniqueID"]
                        }]
                    )
                StudentInfo.update_one(
                        {"uniqueID": data["uniqueID"]},
                        {"$set": {
                            "Streak": data["Streak"],
                        }}
                    )
                print(f"ProgressInfo added successfully")
                return jsonify({"Message": "ProgressInfo Added!"}), 201
        else:
            print("No data found in update_ExistingSubjectsArray route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in update_ExistingSubjectsArray route")
        return jsonify({"error": "An exception occurred in update_ExistingSubjectsArray route"}), 500

@app.route('/GetExistingSubjectsArray', methods=['POST'])
def get_ExistingSubjectsArray():
    try:
        data = request.json
        if data:
            if data["Type"] == "Phone Number":
                existingSubjectsData = SchedulesCompletion.find_one({ "Phone Number": data["Value"] }, {"_id": 0, "Completion": 1})
            elif data["Type"] == "Email ID":
                existingSubjectsData = SchedulesCompletion.find_one({ "Email ID": data["Value"] }, {"_id": 0, "Completion": 1})
                
            if existingSubjectsData:
                print(f"Sended the ExistingSubjectsArray")
                return jsonify(existingSubjectsData["Completion"]), 201
            else:
                print("No existing subjects found")
                return jsonify({"error": "No existing subjects found!"}), 400
        else:
            print("No data found in get_ExistingSubjectsArray route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in get_ExistingSubjectsArray route")
        return jsonify({"error": "An exception occurred in get_ExistingSubjectsArray route"}), 500
    
@app.route('/Testing', methods=['POST'])
def Testing():
    try:
        data = request.json
        if data:
            print(f"Data received in Testing route: {data}")
            return jsonify({"Status": "Data Received!"}, {"Message": data}), 201
        else:
            print("No data found in Testing route")
            return jsonify({"error": "No data found!"}), 400
    except Exception as e:
        print(f"Error: {e}. This is the error in Testing route")
        return jsonify({"error": "An exception occurred in Testing route"}), 500
    
@app.route('/GetVersionInfo', methods=['GET'])
def get_version_info():
    try:
        VersionInfo = [
            {
                "Platform": "android",
                "Versions": {
                    "LatestVersion": "1.6.3",
                    "MinSupportedVersion":"1.6.3",
                    "UpdateRequired": "true"
                }
            },
            {
                "Platform": "ios",
                "Versions": {
                    "LatestVersion": "1.6.0",
                    "MinSupportedVersion": "1.6.0",
                    "UpdateRequired": "true"
                }
            }
        ]
        print(f"Returned Version Info: {VersionInfo}")
        return jsonify(VersionInfo)
    except Exception as e:
        print(f"Error: {e}. This is the error in GetVersionInfo route")
        return jsonify({"error": "An exception occurred in GetVersionInfo route"}), 500
    
# @app.route('/SendingWhatsAppMessage', methods=['POST'])
# def SendingWhatsAppMessage():
#     try:
#         data = request.json
#         if data:
#             message = client.messages.create (
#                 from_="whatsapp:+918052860019",
#                 body="Hello, there!",
#                 to=f"whatsapp:+91{data}",
#             )
#             return jsonify({"message": "WhatsApp Message sent successfully!"}), 201
#         else:
#             return jsonify({"error": "No data found!"}), 400
#     except:
#         return jsonify({"error": "An exception occurred in SendingWhatsAppMessage route"}), 500
        
if __name__=='__main__':
    app.run()
    # app.run(debug=True, host='0.0.0.0')