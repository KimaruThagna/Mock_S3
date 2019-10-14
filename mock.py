import json, os, boto3

'''
Objective. A function that downloads all the .json files uploaded to a specific
folder in an s3 bucket
'''

def download_json_files(bucket, prefix, local_dir):
    bucket = boto3.resource("s3").Bucket(bucket) # initialize resource
    objects = bucket.objects.filter(Prefix=prefix)
    print(objects)
    keys = [obj.key for obj in objects if obj.key.endswith(".json")] # retrieve any item that has the .json extension
    print(keys)
    local_paths = [os.path.join(local_dir, key) for key in keys] # make paths to relevant files on local environment
    for key, local_path in zip(keys, local_paths):
        os.makedirs(os.path.dirname(local_path), exist_ok=True) # make directories
        bucket.download_file(key, local_path) # download file into the local directory