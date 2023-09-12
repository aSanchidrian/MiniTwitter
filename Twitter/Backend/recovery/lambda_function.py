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
    user_phrase="err";
    user_newPass="err";
    
    if "isBase64Encoded" in event:
        isEncoded=bool(event["isBase64Encoded"]);
    
        if isEncoded:
            decodedBytes = base64.b64decode(event["body"]);
            decodedStr = decodedBytes.decode("ascii") ;
            print(json.dumps(parse_qs(decodedStr)));
            decodedEvent=json.loads(json.dumps(parse_qs(decodedStr)));
            user_email=decodedEvent["user_email"][0];
            user_phrase=decodedEvent["user_phrase"][0];
            user_newPass=decodedEvent["user_newPass"][0];

    else:
        user_email=event["body"]["user_email"];
        user_phrase=event["body"]["user_phrase"];
        user_newPass=event["body"]["user_newPass"];
        
    print(user_email);
    print(user_phrase);
    print(user_newPass);
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("select * from users where user_email = '" + user_email + "' and phrase = '" + user_phrase + "'");
            conn.commit();

            user = cur.fetchone();

            if user:
                print("Username = " + user[0]);
                
                with conn.cursor() as cur2:
                    cur2.execute("update users set user_password = '"+user_newPass+"' where user_email = '"+user_email+"'");
                    conn.commit();
                cur.close();
                return {
                    'statusCode': 200,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body' : json.dumps( { 'res': 'OK', 'user_name': "password changed"} )
                }                
            else:
                print("El usuario con email " + user_email + " y pass " + user_pass + " no existe")
                cur.close();
                return {
                    'statusCode': 400,
                    'headers': { 'Access-Control-Allow-Origin' : '*' },
                    'body' : json.dumps( { 'res': 'ERROR', 'message': 'Password recovery phrase incorrect'} )
                }                
                return 

    except pymysql.MySQLError as e:
        print (e)
    conn.close();