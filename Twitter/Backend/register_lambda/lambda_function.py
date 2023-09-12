import pymysql
import json
import base64
from urllib.parse import parse_qs

rds_host = "3.221.116.174"

username = "admin"
password ="password"
dbname = "twitter"

def lambda_handler(event, context):
    print(json.dumps(event));
    
    user_name="err";
    user_email="err";
    user_pass="err";
    user_phrase="err";
    
    if "isBase64Encoded" in event:
        isEncoded=bool(event["isBase64Encoded"]);
    
        if isEncoded:
            decodedBytes = base64.b64decode(event["body"]);
            decodedStr = decodedBytes.decode("ascii") ;
            print(json.dumps(parse_qs(decodedStr)));
            decodedEvent=json.loads(json.dumps(parse_qs(decodedStr)));
            user_name=decodedEvent["user_name"][0];
            user_email=decodedEvent["user_email"][0];
            user_pass=decodedEvent["user_pass"][0];
            user_phrase=decodedEvent["user_phrase"][0];
    else:
        user_name=event["body"]["user_name"];
        user_email=event["body"]["user_email"];
        user_pass=event["body"]["user_pass"];
        user_phrase=event["body"]["user_phrase"];
        
    print(user_name);
    print(user_email);
    print(user_pass);
    print(user_phrase);
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("insert into users values ('" +user_name+"','"+user_email+"','" +user_pass+ "','" +user_phrase+ "')");
            conn.commit();
            cur.close();
    except pymysql.MySQLError as e:
        print (e)
    conn.close();
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body' : json.dumps( { 'res': 'OK'} )
    }
