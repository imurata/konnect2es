from flask import Flask, request, jsonify
import gzip
import json
import os
from elasticsearch import Elasticsearch, TransportError, helpers
import urllib3

# 警告を無視
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Elasticsearchの接続設定
es_host = os.getenv('ELASTICSEARCH_HOST')
api_key = os.getenv('ELASTICSEARCH_API_KEY')
index_name = os.getenv('ELASTICSEARCH_INDEX', 'default-index')

es = Elasticsearch(
    es_host,
    api_key=api_key,
    verify_certs=False,  # 証明書の検証をスキップ
    ssl_show_warn=False
)

@app.route('/webhook', methods=['POST'])
def webhook():
    headers = dict(request.headers)
    print("Received request headers:")
    for key, value in headers.items():
        print(f"  {key}: {value}")

    if request.content_type == 'text/plain':
        data = gzip.decompress(request.data).decode('utf-8')

        print("\nReceived data:")
        print(data)

        try:
            actions = []
            json_objects = data.split('\n')
            for obj in json_objects:
                if obj.strip():
                    json_data = json.loads(obj)
                    # フィールド型の変換
                    if 'trace_id' in json_data:
                        json_data['trace_id'] = str(json_data['trace_id'])
                    # Bulk APIのアクションに追加
                    action = {
                        "_index": index_name,
                        "_source": json_data
                    }
                    actions.append(action)

            # Elasticsearchにデータを一括転送
            success, failed = helpers.bulk(es, actions, raise_on_error=False, raise_on_exception=False)
            if failed:
                print("Failed actions:")
                for fail in failed:
                    print(fail)
                return jsonify({"status": "failed", "reason": "bulk index errors"}), 500

            return jsonify({"status": "success"}), 200
        except json.JSONDecodeError:
            return jsonify({"status": "failed", "reason": "invalid JSON"}), 400
        except TransportError as e:
            print(f"TransportError: {str(e)}")
            return jsonify({"status": "failed", "reason": str(e)}), 500
    return jsonify({"status": "failed", "reason": "invalid content type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
