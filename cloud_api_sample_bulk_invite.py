import urllib
import json
import sys
import AYX_CloudAPI

# ============== このサンプルは何ですか？ ================
# ユーザーを一括招待するコードです
# 1. クラウド設定とトークンをそれぞれ同じフォルダ内のJSONファイルに記載する
# 2. 「設定」のusersに招待したいemailアドレスのリストをカンマ区切りで複数記載
# 3. 本プログラムを実行
# トークン：Cloudの[ユーザー設定]-[OAuth 2.0 APIトークン]から取得し、credential.jsonに記載する
# クラウド設定：cloud_setting.jsonに記載する
# ======================================================

# ============== 設定 ==============
users = ["youremail@example.com"] # 割り当てたいユーザーのemailアドレスのリスト（カンマ区切りで複数指定可能）

# その他設定(固定値)
JSON_FILE_PATH = "credential.json"
CLOUD_SETTING_JSON = "cloud_setting.json"

# ============== 関数 ==============
def invite_users(aac_url, access_token, workspaceid, emails):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "AYX_CloudAPI by AK",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    requestBody = {
        "emails": emails
    }
    # API call
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/people/batch', headers=headers, data=json.dumps(requestBody).encode('utf-8'), method='POST')
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# ============== メインコード ==============
# サンプル設定の場合は実行しない
if users == ["youremail@example.com"]:
    print("サンプルの設定のままです。設定を書き換えて実行してください。")
    sys.exit()

# クラウド設定の読み込み
AYX_CLOUD_URL, REFRESH_URL, OAUTH_CLIENT_ID = AYX_CloudAPI.load_cloud_setting(CLOUD_SETTING_JSON)

# アクセストークン取得（と更新）
access_token = AYX_CloudAPI.update_tokens(REFRESH_URL, OAUTH_CLIENT_ID, JSON_FILE_PATH)

# ワークスペースIDを取得
workspace_info = AYX_CloudAPI.get_current_workspace(AYX_CLOUD_URL, access_token)
workspaceid = workspace_info['id']

# 関数をコール
result = invite_users(AYX_CLOUD_URL, access_token, workspaceid, users)
# 結果（追加されたユーザーのpersonIdが戻り値として取得できます）
print(result)

