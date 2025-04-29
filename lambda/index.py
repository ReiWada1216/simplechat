# lambda/index.py
import json
import urllib.request
import os
import logging

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        user_message = body["message"]

        # Colabサーバーのエンドポイントを環境変数から取得
        url = os.environ.get("COLAB_SERVER_URL", "https://91bf-34-168-103-233.ngrok-free.app/generate")

        # Colab APIが期待するデータ形式に合わせる
        data = json.dumps({"prompt": user_message}).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req) as response:
            response_body = json.loads(response.read())

        # Colabサーバーの返答を取り出す
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

    except json.JSONDecodeError as e:
        logger.error(f"JSONデコードエラー: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "success": False,
                "error": "無効なJSON形式です"
            })
        }
    except urllib.error.URLError as e:
        logger.error(f"URLエラー: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": "サーバーに接続できません"
            })
        }
    except Exception as e:
        logger.error(f"予期せぬエラー: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": "内部サーバーエラーが発生しました"
            })
        }
