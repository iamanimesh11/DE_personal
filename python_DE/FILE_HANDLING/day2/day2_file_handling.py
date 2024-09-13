import logging
import datetime
import os
import re
import string
import time
import pandas as pd
import re
import json

def more_than5000_salary_and_average(filename):
    with open("sample.csv",'r') as file:
        s= file.readlines()
        print(s)
        # for i in range(1,len(s)-1):
        #     print(s[i])
        summ=0
        count=0
        for i in s:
            x=i.split(",")
            try:
                if int(x[-1])>5000:
                    print("below employee earn more than 5000:")
                    print(x[-3].strip())
                summ+= int(x[-1])
                count+=1
            except:
                logging.log(msg="np",level=2)
        print(f"average: {summ/count}")
        x=summ/count
        print("%.1f" % x)

# more_than5000_salary_and_average("sample.csv")
# using logs file to calculate total login and logout

def total_login_logout(filename):
    with open(filename,"r") as file:
        s=file.readlines()
        login=0
        logout=0
        for x in s:
            if x.split()[-1]=="login":
                login+=1
            else:
                logout+=1
        # print("login: {},logout:{}".format(login,logout))
        empty = []
        # for x in s:
        #     empty.append((x.split()))
        # print(x)
        # df = pd.DataFrame(empty, columns=['a','b','c','status'])
        # print(df)
        # print(f"login count: {df["status"].value_counts()['login']}")
        # users_with_login = df[df['status'] == 'login']
        # print(users_with_login)
        # print(users_with_login.shape)
        # r,c=users_with_login.shape

# q 2 :user with their login and logout counts
        users={}
        for  x in s:
            action =x.split()[3]
            user = x.split()[2]
            # print(f"{x}:{action},{user}")
            if action == "login" and user not in users:
                users[user]=action
            if action=="logout" and user in users:
                print(f" users have logged in and out successfully {user}")
 # which user has logged in and logged out
# total_login_logout("logs")
from dateutil import parser

login_times = {}
total_time_logged_in = {}
def time_by_login_logout(filename):

    with open(filename,"r") as file:
        for line in file.readlines():

            action = line.split()[3]
            user = line.split()[2]
            x=line.split()[0]+" " +line.split()[1]

            timestamp = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
            if action =="login":
                login_times[user]=timestamp
            elif action=="logout":
                if user in login_times:
                    time_logged_in=timestamp-login_times[user]

                    if user in total_time_logged_in:
                        total_time_logged_in[user]+=time_logged_in
                    else:
                        total_time_logged_in[user]=time_logged_in

                    del login_times[user]

3# ;
# for user, time in total_time_logged_in.items():
#     print(f"User {user} was logged in for {time}")
##### large file handlin

def report_count_number(directoryName):
    x=datetime.datetime.now()
    total_sum=0
    number_pattern = re.compile(r'\b\d+\b')
    for i in os.listdir(directoryName):
        with open("{}\\{}".format(directoryName,i),"r")as file:
            content=file.read()
            print(content)
            n=map(int,number_pattern.findall((content)))
            total_sum+=sum(n)


    print(total_sum)
    print(datetime.datetime.now()-x)

# report_count_number("reports")

def read_from_json(filename):
    with open(filename)as file:
        data=json.load(file)
        for e in data["employees"]:
            if e["department"]=="Sales":
                print( e["name"])

        new_emp= {"name": "alice", "age": 20, "department": "engg"}

        data['employees'].append(new_emp)
        with open(filename,"w") as file:
            json.dump(data,file,indent=4)

# read_from_json("data.json")
emp={}
def emp_listing(filename):
    with open(filename) as file:
        data = json.load(file)
        for e in data["employees"]:
            d=e["department"]
            name = e["name"]
            if d not in emp:
                emp[d]=[]
                emp[d].append(name)

            else:
                emp[d].append(name)

        for d ,name in emp.items():
            print(f"{d}: {','.join(name)}")

# emp_listing("datajson.")

maxi=0
def highest_Salary(filename):
    with open(filename) as file:
        data = json.load(file)
        for e in data["employees"]:
            salary = e["salary"]
            name = e["name"]
            if salary>maxi:
                max=salary
                h_emp=e["name"]



        print(h_emp,max)

highest_Salary("data.json.")

def remove_emp_Dept(filename):
    with open(filename) as file:
        data = json.load(file)
        for e in data["employees"]:
            dept = e["department"]
            if dept =="HR":
                data["employees"].remove(e)

        with open(filename,"w") as file:
            json.dump(data,file)

remove_emp_Dept("data.json.")