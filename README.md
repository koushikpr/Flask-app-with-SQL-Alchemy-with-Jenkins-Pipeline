# Flask-app-with-SQL-Alchemy-with-Jenkins-Pipeline

This is a simple Flask application that uses FLASK SQL Alchemy to create a Relational DB and store the details of a movie along with specific relationships 

To run the program on your local machine. Run 

```
pip install -r requirements.txt
python app.py
```

To the test the program on your local machine run 
```
pytest test_app.py
```

Furthermore there exists a simple HTML file in the templates folder for front end development as well. 

This app can be further deployed on any other platform either by containerizing it or by hosting it on a cloud platform 

1. Hosting on Docker
```
# Run only on Docker run
docker build .
# Run on Docker-Compose
docker-compose build
docker-compose up
```
2. Hosting on AWS EC2 
To host on EC2 there are 2 configurations to be done. Clone the repo on the EC2 Instance and replace the app.run(debug=True) with app.run(debug=True, host='0.0.0.0'). This will enable it for production environment. then run 
```
pip install -r requirements.txt
python app.py
```
And go to http://{your_public_ip}:5000 to find your hosted app on AWS EC2 Instance

3. Automating the build using Github Webhook and Jenkins
To further host the program for CI/CD Pipeline run the Jenkins Pipeline on your host dashboard. This will automatically run the different stages of Build->Test->Deployment automatically this is a DevOps lifecycle principle. 


