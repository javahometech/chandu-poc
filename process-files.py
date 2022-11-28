import json
import boto3
import os
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")

# TODO remove later
stage = os.environ["stage"]
bucket = os.environ["BUCKET"]
key = os.environ["Key"]
json_file_name = key.split(".")[0]+".json"
# TODO remove later

"""
    Download .txt file from S3 and convert to json and upload it to S3
"""
def str_json():
    obj = s3.Object(bucket, key)
    file_data = obj.get()['Body'].read().decode('utf-8') 
    data = file_data.split(",")
    emp_dict = {
        "Name": data[0],
        "Location": data[1],
        "Company": data[2]
    }
    str_emp = json.dumps(emp_dict)
    with open(json_file_name, "w") as f:
        f.write(str_emp)
    object_name = os.path.basename(json_file_name)
    response = s3_client.upload_file(object_name, bucket, "stage1/"+json_file_name)
    return {
        "Bucket": bucket,
        "Key": "stage1/"+json_file_name
    }

def json_update():
    key = "stage1/"+json_file_name
    obj = s3.Object(bucket, key)
    file_data = obj.get()['Body'].read().decode('utf-8') 
    json_dict = json.loads(file_data)
    json_dict.pop("Location")
    # print(json_dict)
    str_emp = json.dumps(json_dict)
    with open("chandra.json", "w") as f:
        f.write(str_emp)
    object_name = os.path.basename(key)
    response = s3_client.upload_file(object_name, bucket, "stage2/"+json_file_name)
    return {
        "Bucket": bucket,
        "Key": "stage2/"+json_file_name
    }

def change_json_parameters():
    key = "stage2/"+json_file_name
    obj = s3.Object(bucket, key)
    file_data = obj.get()['Body'].read().decode('utf-8') 
    json_dict = json.loads(file_data)
    json_dict["Company"] = "HCL"
    # print(json_dict)
    str_emp = json.dumps(json_dict)
    with open(json_file_name, "w") as f:
        f.write(str_emp)
    object_name = os.path.basename(json_file_name)
    response = s3_client.upload_file(object_name, bucket, "stage3/"+json_file_name)

print(os.environ)

if stage == "stage1":
    print("stage1")
    str_json()
elif stage == "stage2": 
    print("stage2")
    json_update()
elif stage == "stage3": 
    print("stage3")
    change_json_parameters()