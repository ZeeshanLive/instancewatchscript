import boto3
from pprint import pprint
from urllib import request, parse
import json
import logging
logging.basicConfig(level=logging.INFO)
webhook = "https://hooks.slack.com/services/T0"
messages = []

def send_message_to_slack(text):
    post = {"text": "{0}".format(text)}
    print (post)
    try:
        json_data = json.dumps(post)
        req = request.Request(webhook,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))


def lambda_handler(event, context):
    custom_filter = [{
    'Name':'tag:Application', 
    'Values': ['weatherrun']}]
    ec2 = boto3.resource('ec2')
    base = ec2.instances.filter(Filters=custom_filter)
    messages = []
    for instance in base:
        print(instance.launch_time)
        instance_launch_time= date(instance.launch_time.year,instance.launch_time.month,instance.launch_time.day)
        Host_Date = date(time.localtime(time.time()).tm_year,time.localtime(time.time()).tm_mon,time.localtime(time.time()).tm_mday)
        diff = (Host_Date - instance_launch_time)
        #print (diff.days*24)
        #print (messages)
        if (diff.days*24 > 3):
            messages.append("*{}*: is online since {} hours".format(instance.id,diff.days*24))

            #print(instance.id)
            send_message_to_slack()