# -*- coding: utf-8 -*-

import os
import json
import boto3

import datetime
import warnings
import numpy as np
import torch
import time
warnings.filterwarnings("ignore",category=FutureWarning)

from transformers import BertTokenizer
from modeling_cpt import CPTModel, CPTForConditionalGeneration

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
import flask

# The flask app for serving predictions
app = flask.Flask(__name__)

s3_client = boto3.client('s3')

print ("loading pretrained models!")
# Set up model
model = CPTForConditionalGeneration.from_pretrained("6")
tokenizer = BertTokenizer.from_pretrained('6')
#model.eval()  # Set in evaluation mode
print ("<<<< loading pretrained models success")


def cpt_infer(text):
    t1 = datetime.datetime.now()
    
    inputs = tokenizer(text, return_tensors="pt",max_length=512)
    outputs = model.generate(inputs['input_ids'], max_length=64, top_p=0.95)
    generated = tokenizer.decode(outputs[0])

    print("prediction result: ",generated)
    
    t2 = datetime.datetime.now()
    print("<<<<done")
    return generated, str(t2 - t1)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    # health = ScoringService.get_model() is not None  # You can insert a health check here
    health = 1

    status = 200 if health else 404
    print("===================== PING ===================")
    return flask.Response(response="{'status': 'Healthy'}\n", status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def invocations():
    tic = time.time()
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    print("================ INVOCATIONS =================")
    data = flask.request.data.decode('utf-8')
    print("<<<<<input data: ", data)
    
    data = json.loads(data)
    data_input = data['data']

    #inference
    res, infer_time = cpt_infer(data_input)
    
    print("Done inference! ")
    print("res: ", res)
    inference_result = {
        'result': res,
        'infer_time': infer_time
    }
    
    _payload = json.dumps(inference_result, ensure_ascii=False)
    return flask.Response(response=_payload, status=200, mimetype='application/json')
    
    