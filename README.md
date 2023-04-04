# User gallery
## Summary
This app allows user to store, delete and view their images.  
It uses postgres as db and minIO as storage for images.  
For managing minIO storage `django-storages` is used.  
For auto-generation documentation and interactive sandbox for testing requests `drf-yasg` 
lib is used.  
This project uses `pytest` for testing.
## Preparation for use
1. Install python 3.10
2. Install poetry
3. Install docker and docker-compose
## Installation
1. Clone repo to your computer  
`git clone https://github.com/nikitakostolomov/user-gallery.git`
2. Create virtual environment via poetry  
`~/user-gallery$ poetry env use <your python version>`
3. Activate virtual environment  
`~/user-gallery$ poetry shell`
4. Add `backend` dir to your PYTHONPATH
5. Install dependencies  
`poetry install`
## Configure postgres and minIO
1. Build app image  
`~/user-gallery$ docker-compose build`
2. Run docker-compose  
`~/user-gallery$ docker-compose up -d`
3. After previous command django app will not be available, 
because db and bucket for images were not created yet
4. In pgadmin you will need to create db for app:  
   1. Go to http://localhost:5050/browser/
   2. Create master password, when prompted
   3. Click `Add new server`
   4. In `General` tab enter `postgres` in `Name`
   5. Go to `Connection` tab  
      1. In `Hostname/adress` enter `postgres`
      2. In `Maintenance database` enter `postgres`
      3. In `Username` enter `postgres`
      4. In `Password` enter `postgres`
   6. Click `Save`
   7. After that on the left click `Servers`. There should appear `postgres` server
   8. Click on `postgres` server
   9. Right click on `Databases` and select `create`
   10. In `Database` enter `gallery`
5. In minIO you will need to create bucket for app:
   1. Go to http://127.0.0.1:9001/login
   2. Login with username `minioadmin` and password `minioadmin`
   3. Go to `Buckets` tab on the left and create bucket with name `gallery`  
## Two ways to run app
### First way: run app from docker
1. Restart django app in docker-compose  
`~/user-gallery$ docker-compose restart web`
2. After that all migrations should be applied and app is ready for usage
### Second way: run app locally
1. In `.env` file change:
   1. `AWS_S3_ENDPOINT_URL` to `"http://localhost:9000"`
   2. `POSTGRES_HOST` to `localhost`
2. In case migrations were not applied yet, run  
`~/user-gallery$ python backend/manage.py migrate`
3. To start app, run  
`~/user-gallery$ python backend/manage.py runserver`
## Usage
After app has been started, you can go to http://localhost:8000/swagger/  
There will be swagger-ui with all endpoints presented in this app.
You can send requests in interactive mode, thanks to swagger.  
You can also send requests via Postman.
### Register new user
First of all, you will need to register new user and authorize.  
Click on `/register/` endpoint and provide `username` and `password`.  

In Postman send POST request to http://localhost:8000/register/ and 
provide `username` and `password` in request body.
### Authorization
Click authorize button on the top right and provide `username` and `password`. 
After that you can use gallery endpoint to perform CRUD actions with images.  

In Postman send POST request to http://localhost:8000/auth/ and 
provide `username` and `password` in request body. You will get token. 
This token should be used in Header of every request. Now you can click on `Authorization` tab, 
in `Type` select `Bearer Token` and paste given token there.
### Uploading image
Click on `/gallery/images/image` with PUT method and choose image, that you want to upload, and click `Execute`.
In Response you will get link to minIO, where your image is stored. You can copy and paste it in 
address bar of your browser, and you will see your image. Note, that, if you are running app inside docker, you will need
to change `minio` to `localhost` in given link.  

In Postman send PUT request to http://localhost:8000/gallery/images/image and provide image in 
request body. To do that:
1. Go to `Body`
2. Choose `form-data`
3. In `Key` enter `image` and choose `File` type
4. After that in `Value` field you will see prompt to select file  

Do not forget to provide authorization token.
### Viewing images
#### View image by name
Click on `gallery/images/image` with GET method, enter name of uploaded image and click `Execute`.
In Response you will get link to minIO, where your image is stored. You can copy and paste it in 
address bar of your browser, and you will see your image. Note, that, if you are running app inside docker, you will need
to change `minio` to `localhost` in given link.  

In Postman send GET request to http://localhost:8000/gallery/images/image and provide
`image_name` in `Key` field and name of uploaded image in `Value` field in `Query Params`.  
Do not forget to provide authorization token.
#### View all uploaded images for current user
Click on `gallery/images` with GET method and click `Execute`. 
In Response you will get dictionary, where key is name of the image and value is a link to minIO, where your image is stored. 
You can copy and paste it in address bar of your browser, 
and you will see your image. Note, that, if you are running app inside docker, you will need
to change `minio` to `localhost` in given link.  

In Postman send GET request to http://localhost:8000/gallery/images.  
Do not forget to provide authorization token.
### Deleting images
#### Delete image by name
Click on `gallery/images/image` with DELETE method, enter name of uploaded image and click `Execute`.
Response will be empty with status code 204.

In Postman send DELETE request to http://localhost:8000/gallery/images/image and provide
`image_name` in `Key` field and name of uploaded image in `Value` field in `Query Params`.  
Do not forget to provide authorization token.
#### Delete all images
This action requires admin rights, so to perform it, you will need to:
1. Create superuser
   1. Go to terminal
   2. Enter command  
   `~/user-gallery$ python backend/manage.py createsuperuser`
   3. Complete user creation and remember credentials
2. Authorize with entered credentials  

After that click on `gallery/images/delete` with DELETE method and click `Execute`.
Response will be empty with status code 204.

In Postman send DELETE request to http://localhost:8000/gallery/images/delete.  
Do not forget to provide authorization token.

## Testing
To run integration tests you will need to configure `.env` file like in 
[this section](#second-way-run-app-locally).  
Note, that in order to run integration tests, 
postgres and minIO should be running at the background. Unit tests do not require any 
running services. 

To run unit and integration tests, enter  
`~/user-gallery$ pytest`  

To run unit tests, enter  
`~/user-gallery$ pytest -m unit`  

To run integration tests, enter  
`~/user-gallery$ pytest -m integration`