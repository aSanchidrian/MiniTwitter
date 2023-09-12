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
    
    messageId="err";
    likes="err";
    dislikes="err";
    
    if "isBase64Encoded" in event:
        isEncoded=bool(event["isBase64Encoded"]);
    
        if isEncoded:
            decodedBytes = base64.b64decode(event["body"]);
            decodedStr = decodedBytes.decode("ascii") ;
            print(json.dumps(parse_qs(decodedStr)));
            decodedEvent=json.loads(json.dumps(parse_qs(decodedStr)));
            user_email=decodedEvent["messageId"][0];
            user_phrase=decodedEvent["likes"][0];
            user_newPass=decodedEvent["dislikes"][0];

    else:
        user_email=event["body"]["messageId"];
        user_phrase=event["body"]["likes"];
        user_newPass=event["body"]["dislikes"];
        
    print(messageId);
    print(likes);
    print(dislikes);
    
    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("update posts set likes = '"+likes+"', dislikes = '"+dislikes+"' where messageId = '"+messageId+"'");
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