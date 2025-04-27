# lambda/index.py
import json
import urllib.request

def handler(event, context):
    body = json.loads(event["body"])
    user_message = body["message"]

    url = "https://9b26-34-87-137-199.ngrok-free.app/chat"  # ← あなたのColabサーバーURL！

    data = json.dumps({"message": user_message}).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        response_body = json.loads(response.read())

    answer = response_body["answer"]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps({
            "success": True,
            "response": answer
        })
    }

