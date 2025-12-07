import urllib
import json
import AYX_CloudAPI

# ============== このサンプルは何ですか？ ================
# 一括でロールをユーザーに割り当てるコードです
# 1. クラウド設定とトークンをそれぞれ同じフォルダ内のJSONファイルに記載する
# 2. 「設定」でpolicyIdと割り当てたいユーザーのリストを記載
# 3. 本プログラムを実行
# トークン：Cloudの[ユーザー設定]-[OAuth 2.0 APIトークン]から取得し、credential.jsonに記載する
# クラウド設定：cloud_setting.jsonに記載する
# ======================================================

# ============== 設定 ==============
policyId = 33278 # 割り当てたいロールのpolicyId
users = [1302] # 割り当てたいユーザーID（personId）のリスト（カンマ区切りで複数指定可能）

# その他設定(固定値)
JSON_FILE_PATH = "credential.json"
CLOUD_SETTING_JSON = "cloud_setting.json"

# ============== 関数 ==============
def assign_role_to_users(aac_url, access_token, policyId, users):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "AYX_CloudAPI by AK",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    requestBody = users
    # API call
    request = urllib.request.Request(f'{aac_url}/iam/v1/authorization/roles/{policyId}/people', headers=headers, data=json.dumps(requestBody).encode('utf-8'), method='PUT')
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# ============== メインコード ==============
# クラウド設定の読み込み
AYX_CLOUD_URL, REFRESH_URL, OAUTH_CLIENT_ID = AYX_CloudAPI.load_cloud_setting(CLOUD_SETTING_JSON)

# アクセストークン取得（と更新）
access_token = AYX_CloudAPI.update_tokens(REFRESH_URL, OAUTH_CLIENT_ID, JSON_FILE_PATH)

# 関数をコール
result = assign_role_to_users(AYX_CLOUD_URL, access_token, policyId, users)
# 結果（ただし、結果の確認方法がないので、実際にワークスペースを開いて確認してください）
print(result)

