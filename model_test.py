from rasa_nlu.model import Interpreter
import json, mysql.connector
import string


interpreter = Interpreter.load("./model")
message = "What is the make of this car?"
print(message)
result = interpreter.parse(message)
#print(json.dumps(result, indent=2))
intent=result["intent"]["name"]

flag=0
for e in result["entities"]:
	if e["entity"]=="attribute":
		flag=1
		val=e["value"]
print("Intent: ",intent)
if flag==1:
	print("Attribute: ",val)
sno = 8
if intent=="search_db":
	#print("SELECT `"+str.capitalize(val)+"` FROM carsdb WHERE Make='"+model+"'")

	cardb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="123456",
		database="projectvqa")

	dbcursor = cardb.cursor()
	dbcursor.execute("SELECT `"+str.capitalize(val)+"` FROM carsdb WHERE `Serial Number`="+str(sno)+"")
	dbresult = dbcursor.fetchall()
	print("Answer: "+str(dbresult[0][0]))