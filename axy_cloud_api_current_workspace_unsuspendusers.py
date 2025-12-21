import axycloudapi
import csv
from collections import defaultdict

# ============== このサンプルは何ですか？ ================
# 取得したOAuth2.0 APIトークンに応じたワークスペースのユーザーをサスペンドから復帰するコードです
# 1. クラウド設定とトークンをそれぞれ同じフォルダ内のJSONファイルに記載する
# 2. サスペンドから復帰対象のユーザーをunsuspend_user_list.csvに記載する
# 3. 本プログラムを実行
# トークン：Cloudの[ユーザー設定]-[OAuth 2.0 APIトークン]から取得し、credential.jsonに記載する
# クラウド設定：cloud_setting.jsonに記載する
# ======================================================
# 設定
UNSUSPEND_USER_LIST = "unsuspend_user_list.csv"

# その他設定(固定値)
JSON_FILE_PATH = "credential.json"
CLOUD_SETTING_JSON = "cloud_setting.json"

# ============== メインコード ==============
# クラウド設定の読み込み
AYX_CLOUD_URL, REFRESH_URL, OAUTH_CLIENT_ID = axycloudapi.load_cloud_setting(CLOUD_SETTING_JSON)

# アクセストークン取得（と更新）
access_token = axycloudapi.update_tokens(REFRESH_URL, OAUTH_CLIENT_ID, JSON_FILE_PATH)

# ワークスペース情報取得
## 現在のワークスペースIDを取得
current_workspace_info = axycloudapi.get_current_workspace(AYX_CLOUD_URL, access_token)
current_workspace_id = current_workspace_info['id']
print(f"現在のワークスペース：{current_workspace_id}")

# サスペンド対象のリストを取得(ワークスペースIDごとにリスト化)
grouped_data = defaultdict(list)
with open(UNSUSPEND_USER_LIST, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ws_id = row['workspaceId']
        u_id = row['userId']
        
        # workspaceIdをキーにして、userIdをリストに追加していく
        grouped_data[ws_id].append(u_id)

for ws_id, user_ids in grouped_data.items():
    if str(ws_id) == str(current_workspace_id):
        print(f"対象workspaceId: {ws_id}")
        print(f"対象ユーザー数: {len(user_ids)}名")

        response = axycloudapi.set_unsuspend_users(AYX_CLOUD_URL, access_token, current_workspace_id, user_ids)
        print(f"ユーザーアンサスペンドのレスポンス：")
        print(response)
    else:
        print(f"workspaceId{ws_id}は異なるワークスペースのため処理をスキップします。")

