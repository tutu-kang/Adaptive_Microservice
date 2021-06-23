# usage:

#python generate_test_case.py <output_file>
#output_format 

#test_id, #duration, #rate, #connection, #zone, #interference_level, #cart,#catalogue,#shipping,#start_pos, #end_pos


import sys
from datetime import date 
import hashlib
duration = 120 #sec


def getClusterConfiguration(cntCart=1,cntCatalogue=1,cntShipping=1,cntPayment=1,cntRatings=2,cntUser=2, cntWeb=2):
    pods = {}
    pods['cart'] = cntCart
    pods['catalogue'] = cntCatalogue
    pods['shipping'] = cntShipping
    pods['payment'] = cntPayment
    pods['ratings'] = cntRatings
    pods['user'] = cntUser
    pods['web'] = cntWeb


    return pods

def getConfigHash(pods):
    result = 0
    for k in sorted(pods.keys()):
        result *= 10
        result += pods[k]
    
    return result 

start_position = 3
end_position = 22

output_file = "default_test_case.csv"

zones = ['red', 'green','blue', 'yellow']

interference_level = ['none', 'low','medium'] #,'high']
interference_type = ['stream', 'iperf']
#interference_type = ['iperf']


connections = [10, 20, 30]

workflow = ["cart", "catalogue", "ratings", "user", "shipping", "payment"]

# variables - zone, interference_level, connection


def produce(shipping=4, ratings=3):


    paramCnt = {}
    for pod in workflow:
        paramCnt[pod] = 2
    paramCnt['cart'] = 1
    paramCnt['shipping'] = shipping
    paramCnt['ratings'] = ratings


    for work in ["cart", "catalogue", "payment", "user"]:#"ratings", "shipping"]:
        for cnt in [2, 3, 4]:
            paramCnt[work] += 1
            if paramCnt[work] == 5:
                paramCnt[work] = 4
                continue 
            if work == "user" and paramCnt["user"] == 4:
                paramCnt["user"] = 3
                continue 
            for zone in zones:
                for i_type in interference_type:
                    for i_level in interference_level:
                        for con in connections:
                            today = date.today()
                            date_prefix = today.strftime("%b%d")
                            configuration = getClusterConfiguration(cntCart = paramCnt["cart"], cntCatalogue = paramCnt["catalogue"], cntShipping = paramCnt["shipping"],
                            cntPayment = paramCnt["payment"], cntUser=paramCnt["user"])

                            test_id = "{}_{}_{}_{}_{}_{}".format(date_prefix,zone,con, i_type, i_level, getConfigHash(configuration) )
                            data = "{}/{}/{}/{}/{}/{}/{}/{}/{}\n".format(test_id,duration,i_type,con,zone,i_level,configuration,start_position,end_position)                             
                            f.write(data)

    print("test")
with open(output_file,'a' )as f:
    f.write("#test_id/duration/rate/con/zone/i_level/{configuration}/start_position/end_position\n")
    produce()
    produce(shipping=3, ratings=3)
    produce(shipping=3, ratings=2)

