# Packages for Flask App
from flask import Flask,redirect,url_for,render_template,request,session,flash
from pyathena import connect
import boto3
dynamodb=boto3.resource('dynamodb',aws_access_key_id='AKIAXCLY6ZJFXYZ4WN7N',aws_secret_access_key='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',region_name='us-east-1')
dynamoTable=dynamodb.Table('userdetails')

#Connection For AWS S3 Bucket
# Used pyathena module python
cursor = connect(aws_access_key_id='AKIAXCLY6ZJFXYZ4WN7N',
                 aws_secret_access_key='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',
                 s3_staging_dir='s3://zappa-9huhuuh3q/',
                 region_name='us-east-1').cursor()


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("main.html")

@app.route("/new", methods= ["POST","GET"])  
def mainfeature():
  if request.method == "POST":
     user_name=request.form['list8']
     age_group=int(request.form['list1']) 
     travel_select=int(request.form['list2'])
     smoking_select=int(request.form['list3'])
     alchohol_select=int(request.form['list4'])
     occupation_select=int(request.form['list5'])
     distance_select=int(request.form['list6'])

    
     sum=age_group+travel_select+smoking_select+alchohol_select+occupation_select+distance_select
     dynamoTable.put_item(
        Item= {
             'Name':user_name,
             'Age': age_group,
             'TravelStatus':travel_select,
             'Smoking Status':smoking_select,
             'AlcoholStatus':alchohol_select,
             'OccupationStatus':occupation_select,
             'DistanceStatus':distance_select
         }

     )
     
     cursor.execute(f"SELECT rating FROM scoringdata.scoringtable where score={sum}")
     x=cursor.fetchone()
     finx=str(x)[1:-1]
     return render_template('new.html',sum=sum,finx=finx)
    

if __name__ == "__main__":        
    app.run(debug=True)             