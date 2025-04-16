a = {"Name": "John Doe", "Phone Number": "1234567890", "uniqueID": "12345"}
b = {}
if a:
    a["uniqueID"] = "54321"
    b = a

print(b)