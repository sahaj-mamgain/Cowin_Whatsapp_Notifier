import os
import requests
import json
import tabulate
from datetime import datetime, timedelta
# from twilio.rest import Client

# account_sid = 'ACc'
# auth_token = '6f'
# client = Client(account_sid, auth_token)


def return_json(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
    resp = requests.get(url, headers=header)
    return resp.json()


def Table_FromDicList(table):
    head = table[0].keys()
    rows = [x.values() for x in table]
    mess = tabulate.tabulate(rows, head)
    print(mess)


def Sdic(st):
    return {"State": st["state_name"], "ID": st["state_id"]}


def get_state(stateID):
    for st in stateID["states"]:
        yield Sdic(st)


def Ddic(dt):
    return {"State": dt["district_name"], "ID": dt["district_id"]}


def get_district(districtID):
    for dt in districtID["districts"]:
        yield Ddic(dt)


def find_DID():
    states = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    sid = return_json(states)
    State_List = [state for state in get_state(sid)]
    print()
    Table_FromDicList(State_List)
    print()
    state_id = int(input("Enter State ID: "))
    districts = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(
        state_id)
    did = return_json(districts)
    District_List = [district for district in get_district(did)]
    print()
    Table_FromDicList(District_List)
    print()


def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"]}


def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session_info(center, session)


def check_byDistrict(date):
    find_DID()
    district_id = int(input("Enter District Code: "))
    print()
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
        district_id, date.strftime("%d-%m-%Y"))
    return (get_data(url))


def check_byPin(date):
    district_pin = int(input("Enter Pincode: "))
    print()
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
        district_pin, date.strftime("%d-%m-%Y"))
    return (get_data(url))


def check_byLocation():
    Lat = "30.710490"
    Lon = "76.852390"
    latlong = "https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong?lat={}&long={}".format(
        Lat, Lon)
    resp = return_json(latlong)
    print(resp.json())


def get_data(url):
    data = return_json(url)
    return [session for session in get_sessions(data) if session["capacity"] > 0 and session["age_limit"] == 18]


print("Welcome to Slot Notifier!")
print()
print("1)Notify By District Code")
print("2)Notify By Pincode")
print("3)Notify By Location (Coming Soon)")
print()

choice = int(input("Enter your choice: "))
print()


if(choice == 1):
    dataset = check_byDistrict(datetime.today())
elif(choice == 2):
    dataset = check_byPin(datetime.today())
else:
    print("Invalid Choice! Try again")


if not dataset:
    print("Sorry! No Vaccines Avalible.")
else:
    Table_FromDicList(dataset)
    # message = client.messages.create(
    #     from_='whatsapp:+2',
    #     body="Vaccine slo1s Avalible!",
    #     to='whatsapp:+91'
    # )
