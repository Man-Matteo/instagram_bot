import requests
import json
import time

#------------------------------DEFINE VARIABLES FOR POST REQUEST--------------------------------------#

API_KEY =  "c91f2c5a-8dba-4db0-9876-cddb7eb9eaa9" #API key from tryleap.ai

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"   # f is used for strign formatting, allowing to create a single string joining strings and variables
}

IMAGES = [
    #link to images.
    #The more, the better
]

#-----------------------------CREATING A MODEL USING TRYLEAP.AI----------------------------------------#

def create_model(title):
    url = "https://api.tryleap.ai/api/v1/images/models"
    #url for creating a model

    payload = {
        "title": title,
        "subjectKeyword": "@me"
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    #url is site url, mandatory
    #json is the object sent to the site, in this case the struct payload (a dictionary)
    # HTTP headers sent to the url
        #acept indicates what the client is able to understand
        #content-type indicates the type of the resource sent - application/json indicates the object is a json
        #authorization is used to provide credentials that authenticate the user with the server. bearer is an authentication scheme
    #response contains a request.Response object

    model_id = json.loads(response.text)["id"]
    #response.text contains the content of the response
    #loads tronsform a json in a dictionary
    #i'll obtain [id : text], (my ID)
    return model_id

#-----------------------------UPLOADING SAMPLE IMAGES FOR THE MODEL-------------------------------------------#


def upload_image_samples(model_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/samples/url"
    #url to upload images to the model

    payload = {"images": IMAGES}
    response = requests.post(url, json=payload, headers=HEADERS)

#-----------------------------EXECUTE THE MODELING BASED ON THE UPLOADED IMAGES------------------------------#

def queue_training_job(model_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/queue"
    response = requests.post(url, headers=HEADERS)
    data = json.loads(response.text)

    print(response.text)

    version_id = data["id"]
    status = data["status"]

    print(f"Version ID: {version_id}. Status: {status}")

    return version_id, status

#-------------------------------VERSION OF THE MODEL INCLUDING THE STATUS----------------------------------------#

def get_model_version(model_id, version_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/versions/{version_id}"
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)

    version_id = data["id"]
    status = data["status"]

    print(f"Version ID: {version_id}. Status: {status}")

    return version_id, status

#-------------------------------GENERATING THE IMAGE----------------------------------------#

def generate_image(model_id, prompt):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences"

    payload = {
        "prompt": prompt, #description of the image that has to be created
        "steps": 50, #the number of steps to use for the inference.  ??????
        "width": 1920,
        "height": 1080,
        "numberOfImages": 1,
        "seed": 4523184
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    data = json.loads(response.text)

    inference_id = data["id"]   #saving inference id
    status = data["status"]

    print(f"Inference ID: {inference_id}. Status: {status}")

    return inference_id, status

#----------------------------OBTAIN THE IMAGE---------------------------------------#

def get_inference_job(model_id, inference_id):
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences/{inference_id}"

    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)

    inference_id = data["id"]
    state = data["state"]
    image = None

    if len(data["images"]):   #len returns the lenght of an object
        image = data["images"][0]["uri"]

    print(f"Inference ID: {inference_id}. State: {state}")

    return inference_id, state, image

#---------------------------SAVING THE IMAGE LOCALLY----------------------------------------#

def save_image(inference_id, file_path):
    url = f"https://api.tryleap.ai/api/v1/images/inferences/{inference_id}/download"

    response = requests.get(url, stream=True, headers=HEADERS)

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f"Image saved to {file_path}")


#------------------------------CREATE, UPLOAD AND TRAIN-------------------------------------#

model_id = create_model("Sample")
upload_image_samples(model_id)

version_id, status = queue_training_job(model_id)
#wait checking the model status, until he's "finished" training
while status != "finished":
    time.sleep(10)
    version_id, status = get_model_version(model_id, version_id)

#-----------------------------GENERATING THE IMAGE-------------------------------------------#

inference_id, status = generate_image(
    model_id,
    prompt=input()
)
while status != "finished":
    time.sleep(10)
    inference_id, status, image = get_inference_job(model_id, inference_id)

print(image)

file_path = r"C:\Users\hp\Desktop\bot\image.jpg" #r allows to skip escape character for the \
save_image(inference_id, file_path)
