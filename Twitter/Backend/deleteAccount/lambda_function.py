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
    
    user_email="err";
    user_pass="err";
    
    if "isBase64Encoded" in event:
        isEncoded=bool(event["isBase64Encoded"]);
    
        if isEncoded:
            decodedBytes = base64.b64decode(event["body"]);
            decodedStr = decodedBytes.decode("ascii") ;
            print(json.dumps(parse_qs(decodedStr)));
            decodedEvent=json.loads(json.dumps(parse_qs(decodedStr)));
            user_email=decodedEvent["user_email"][0];
            user_pass=decodedEvent["user_pass"][0];
    else:
        user_email=event["body"]["user_email"];
        user_pass=event["body"]["user_pass"];
        
    print(user_email);
    print(user_pass);
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("select * from users where user_email = '" + user_email + "'");
            conn.commit();

            user = cur.fetchone();

            if user:
                print("Username = " + user[0]);
                
                with conn.cursor() as cur2:
                    cur2.execute("DELETE FROM users WHERE user_email = '"+user_email+"';");
                    conn.commit();
                cur.close();
                return {
                    'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body' : json.dumps( { 'res': 'OK', 'user_name': "deleted"} )
                }                
            else:
                print("El usuario con email " + user_email + " y pass " + user_pass + " no existe")
                cur.close();
                return {
                    'statusCode': 400,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body' : json.dumps( { 'res': 'ERROR', 'message': 'El usuario no existe'} )
                }           

    except pymysql.MySQLError as e:
        print (e)
    conn.close();