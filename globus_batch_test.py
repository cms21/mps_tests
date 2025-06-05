from globus_compute_sdk import Client
#from dotenv import load_dotenv
import os
import argparse

import json

gc = Client()

function_id='1986d8b1-a153-4ae4-9ece-9b0a1f5671d0'
endpoint_id='3c8fa332-75a0-4ae9-99ec-f361de20736b'

def run_batch(nbatch=200):


    print(function_id)
    #function_id = os.getenv("FUNCTION_ID")
    #endpoint_id = os.getenv("ENDPOINT_ID")

    batch = gc.create_batch()
    bin_path="/eagle/IRIBeta/fusion/bin"
    
    for i in range(nbatch):
        run_dir=f'/eagle/IRIBeta/csimpson/mps_ionorb_test/test/100_{i}'
        batch.add(args=(run_dir,bin_path),function_id=function_id)
 
    batch_ret = gc.batch_run(endpoint_id,batch=batch)
    with open(f"globus_batch_test_{nbatch}.json","w") as f:
        json.dump(batch_ret,f)
    
    return batch_ret

def arg_parse():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--type', default='idl', help=f'Language for hello', choices=["idl","python"])
    return parser.parse_args()
    
if __name__ == '__main__':

    #args = arg_parse()

    run_batch(nbatch=32)
