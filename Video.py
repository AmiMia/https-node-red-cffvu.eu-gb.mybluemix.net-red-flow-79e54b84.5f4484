import cv2
import numpy as np
import datetime
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
​
# Constants for IBM COS values
COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID="DZp58AEGFbFEhiBXPeYudZG7bDtadcYo9G4fHY4bSs60"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/d38373b6f7e44075959a0a0a10698b43:6ebd11cb-21a1-4cc8-8071-57f4874687e7::"
COS_AUTH_ENDPOINT="https://iam.cloud.ibm.com/identity/token"
​
fire_classifier=cv2.CascadeClassifier("Fire_504844078")

client = Cloudant("56f892ad-b4d6-4db7-9c18-c9c1106ead60-bluemix", "95e439c7361c23f011a18bf475c0ab39399f0a6695ac95af8f1557d807acaf44", url="https://56f892ad-b4d6-4db7-9c18-c9c1106ead60-bluemix:95e439c7361c23f011a18bf475c0ab39399f0a6695ac95af8f1557d807acaf44@56f892ad-b4d6-4db7-9c18-c9c1106ead60-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()
​
database_name="firef1"
​
my_database=client.create_database(database_name)
​
if my_database.exists():
   print(f"'{database_name}' Successfully created.")
​

new_document = my_database.create_document(json_document)

if new_document.exists():
    print(f"Document '{ json_document}' successfully created.")


cos=ibm_boto3.resource("s3", ibm_api_key_id=COS_API_KEY_ID, ibm_service_instance_id=COS_INSTANCE_CRN, ibm_auth_endpoint=COS_AUTH_ENDPOINT, config=Config(signature_version="cffvu"), endpoint_url=COS_ENDPOINT)
​
def multi_part_upload(bucket_name, item_name, file_path):
   try:
      print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
      part_size=1024 * 1024 * 5
      file_threshold=1024 * 1024 * 15
      transfer_config=ibm_boto3.s3.transfer.TransferConfig( multipart_threshold=file_threshold, multipart_chunksize=part_size)
      with open(file_path, "rb") as file_data: cos.Object(bucket_name, item_name).upload_fileobj( Fileobj=file_data, Config=transfer_config)
      print("Transfer for {0} Complete!\n".format(item_name)
      except ClientError as be:
         print("CLIENT ERROR: {0}\n".format(be))
      except Exception as e:
         print("Unable to complete multi-part upload: {0}".format(e))
video=cv2.VideoCapture(0)
​
while True:
   check,frame=video.read()
   gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   fire=fire_classifier.detectMultiScale(gray,1.3,5)
    
    

for(x,y,w,h) in fire:
   cv2.rectangle(frame, (x,y), (x+w,y+h), (127,0,255), 2)
   cv2.imshow('Fire detection', frame)
   picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
   cv2.imwrite(picname+".jpg",frame)
   multi_part_upload("firef1",picname+".jpg",picname+".jpg")
   json_document={"link": COS_ENDPOINT+"/"+"firef"+"/"+picname+".jpg"}
   new_document = my_database.create_document(json_document)

# Check that the document exists in the database.
if new_document.exists():
   print(f"Document '{json_document}' successfully created.")
​
#drawing boundries for detected
for(ex,ey,ew,eh) in eyes:
   cv2.rectangle(frame, (ex,ey), (ex+ew,ey+eh), (127,0,255), 2)
   cv2.imshow('Fire detected', frame)
​
#waitKey(1)- for every 1 millisecond new frame will be captured
Key=cv2.waitKey(1)
if Key==ord('q'):
   video.release()
   cv2.destroyAllWindows()
   break







































