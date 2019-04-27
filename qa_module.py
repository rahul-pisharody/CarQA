from rasa_nlu.model import Interpreter
import json, mysql.connector
import sys


def get_serial():
    return 170



def intent_parse(msg):
    interpreter = Interpreter.load("./newmodel")
    result = interpreter.parse(msg)
    return result["intent"]["name"],result["intent"]["confidence"]

def get_db_query(sno,intent):
    
    db_query = "SELECT "
    if intent=="get_make":
        db_query+="`Make` "
    elif intent=="get_model":
        db_query+="`Model` "
    elif intent=="get_type":
        db_query+="`Type` "
    elif intent=="get_year":
        db_query+="`Year` "
    elif intent=="get_drivetrain":
        db_query+="`Drivetrain` "
    elif intent=="get_power":
        db_query+="`Power(hp)` "
    elif intent=="get_cylinders":
        db_query+="`Cylinders` "
    elif intent=="get_engine_disp":
        db_query+="`Displacement(Litres)` "
    elif intent=="get_seating":
        db_query+="`Seating` "
    elif intent=="get_torque":
        db_query+="`Torque(lbs-ft)` "
    elif intent=="get_mileage":
        db_query+="`Mileage-city(miles/gallon)` "
    elif intent=="get_fuel_capacity":
        db_query+="`Fuel Tank Capacity(gal)` "
    elif intent=="get_wheelbase":
        db_query+="`Wheelbase(inches)` "
    elif intent=="get_ground_clearance":
        db_query+="`Ground Clearance(inch)` "
    elif intent=="get_curb_weight":
        db_query+="`Curb weight(lbs)` "
    elif intent=="get_dimensions":
        db_query+="`Length(inch)`,`Width(inch)`,`Height(inch)` "
    else:
        return ""
    db_query+="FROM ncarsdb WHERE `Serial Number`="+str(sno)
    return db_query

def exec_db_query(dbq):
    cardb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="123456",
      database="projectvqa")

    dbcursor = cardb.cursor()
    dbcursor.execute(dbq)
    return dbcursor.fetchone()

def get_msg_unit(intent):
    msg = ""
    unit = ""
    if intent=="get_make":
        msg="The make of the car is "
    elif intent=="get_model":
        msg="The model of the car is "
    elif intent=="get_type":
        msg="This car is of type "
    elif intent=="get_year":
        msg="This car was made in "
    elif intent=="get_drivetrain":
        msg="This car is "
    elif intent=="get_power":
        msg="This car's engine power is "
        unit="hp"
    elif intent=="get_cylinders":
        msg="This car has "
        unit="cylinders"
    elif intent=="get_engine_disp":
        msg="The engine-displacement is "
        unit="L"
    elif intent=="get_seating":
        msg="This car can seat "
        unit="people"
    elif intent=="get_torque":
        msg="This car has a torque of "
        unit="lbs-ft"
    elif intent=="get_mileage":
        msg="This car has a mileage of "
        unit="miles/gallon"
    elif intent=="get_fuel_capacity":
        msg="This car has a fuel capacity of "
        unit="L"
    elif intent=="get_wheelbase":
        msg="This car has a wheelbase of length "
        unit="inches"
    elif intent=="get_ground_clearance":
        msg="This car has a ground clearance of "
        unit="inches"
    elif intent=="get_curb_weight":
        msg="This car weighs "
        unit="lbs"
    elif intent=="get_dimensions":
        msg="The car has the following dimensions: "
        unit="inches"
    return msg,unit

print("READY")
message=input()

intent,conf = intent_parse(message)
#print("Intent: ",intent," Confidence: ",conf)
if conf<0.25:
    print("Could not determine question")
    sys.exit()

sno = get_serial()
res = 0
if intent[0:3]=="get":
    dbq = get_db_query(sno,intent)
    res=exec_db_query(dbq)
    #print("Ans: "+str(res))

print()
mess,unit=get_msg_unit(intent)
if intent=="get_dimensions":
    print(mess+str(res[0])+"x"+str(res[1])+"x"+str(res[2])+" "+unit)
else:
    print(mess+str(res[0])+" "+unit)
