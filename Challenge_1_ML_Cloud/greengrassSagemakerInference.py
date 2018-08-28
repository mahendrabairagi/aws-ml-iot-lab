#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassSagemakerInference.py

from threading import Timer
import time
import datetime
import cv2
import numpy as np
import json
import os
import sys
import greengrasssdk
import urllib
import zipfile

#boto3 is not installed on device by default.

boto_dir = '/tmp/boto_dir'
if not os.path.exists(boto_dir):
    os.mkdir(boto_dir)
urllib.urlretrieve("https://s3.amazonaws.com/dear-demo/boto_3_dist.zip", "/tmp/boto_3_dist.zip")
with zipfile.ZipFile("/tmp/boto_3_dist.zip", "r") as zip_ref:
    zip_ref.extractall(boto_dir)
sys.path.append(boto_dir)

import boto3
client = greengrasssdk.client('iot-data')

# Creating a greengrass core sdk client

def greengrassSagemakerInference_run():
    vidcap=cv2.VideoCapture(0)
    vidcap.open(0)
    #this may be required if camera needs warm up.
    sleep(1) 
    retval, image = vidcap.read()
    vidcap.release()
    image = cv2.resize(image, (300, 300))
    image = json.dumps(image.tolist())

    endpoint_name = "sagemaker-mxnet-xxxx-xx-xx-xx-xx-xx-xxx"
    runtime = boto3.client('runtime.sagemaker',region_name='us-east-1' )

    response = runtime.invoke_endpoint(EndpointName=endpoint_name,ContentType='application/jsonlines', Body=image)
    result = response['Body'].read()
    client.publish(topic='ModelInference', payload="success")
    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrassSagemakerInference_run).start()
    
# Execute the function above
greengrassSagemakerInference_run()

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
