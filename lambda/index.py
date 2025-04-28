# lambda/index.py
import json
import urllib.request

def handler(event, context):
    body = json.loads(event["body"])
    user_message = body["message"]

    # Colabサーバーのエンドポイント
    url = "https://59e7-34-125-185-254.ngrok-free.app/generate"

    # Colab APIが期待するデータ形式に合わせる（promptにする）
    data = json.dumps({"prompt": user_message}).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        response_body = json.loads(response.read())

    # Colabサーバーの返答を取り出す（適宜合わせる）
    answer = response_body.get("answer") or response_body.get("generated_text") or "No answer received."

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
