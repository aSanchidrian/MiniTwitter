import sys
import logging
import pymysql
import json
import base64
from urllib.parse import parse_qs

rds_host = "3.221.116.174"

username = "admin"
password ="password"
dbname = "twitter"

bucketUrl = "https://asanchidrian1.s3.us-east-1.amazonaws.com/"

def lambda_handler(event , context):
    print(json.dumps(event));
    
    user="err";
    
    if "isBase64Encoded" in event:
        isEncoded=bool(event["isBase64Encoded"]);
    
        if isEncoded :
            decodedBytes = base64.b64decode(event["body"]);
            decodedStr = decodedBytes.decode("ascii") ;
            print(json.dumps(parse_qs(decodedStr)));
            decodedEvent=json.loads(json.dumps(parse_qs(decodedStr)));
            user=decodedEvent["user"][0];
            
    else:
        user=event["body"]["user"];
        
    print(user);
  
    commentList="{\"posts\": [";
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
        print(1);
        with conn.cursor() as cur:
            cur.execute("select * from posts where username='"+user+"'");
            print(2);
            rows = cur.fetchall()
            print(3);
            for row in rows:
                commentList+="{ \"messageId\": \""+str(row[0])+"\", \"comment\": \""+row[2].replace("\n","\\n")+"\", \"attachment\": \""+row[3]+"\", \"likes\": \""+str(row[4])+"\", \"dislikes\": \""+str(row[5])+"\"},";
                    
            commentList=commentList[:-1]+"]}";
            cur.close();
            print(commentList);
    except pymysql.MySQLError as e:    
        print (e)
    conn.close();
    print(4);
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body' : commentList    }
