import json
import requests
import logging
import boto3
import os
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
################ Main handler #########################
def proyecto(event, context):
    print('hola mundo')
   