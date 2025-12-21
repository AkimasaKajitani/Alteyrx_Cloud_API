import axycloudapi
import csv
from collections import defaultdict

# ============== このサンプルは何ですか？ ================
# 取得したOAuth2.0 APIトークンに応じたワークスペースのユーザーのロールを削除・追加します
# 1. クラウド設定とトークンをそれぞれ同じフォルダ内のJSONファイルに記載する
# 2. 対象のユーザーをuser_role_list.csvに記載する
# 3. 本プログラムを実行
# トークン：Cloudの[ユーザー設定]-[OAuth 2.0 APIトークン]から取得し、credential.jsonに記載する
# クラウド設定：cloud_setting.jsonに記載する
# ======================================================
# 設定
USER_LIST = "user_role_list.csv"

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

# 管理対象のリストを取得(ワークスペースIDごとにリスト化)
delete_list = defaultdict(list)
add_list = defaultdict(list)

with open(USER_LIST, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ws_id = row['workspaceId'].strip()
        r_id = row['roleId'].strip()
        u_id = row['userId'].strip()
        action = row['action'].strip().lower()
        if action == "delete":
            delete_list[(ws_id,r_id)].append(u_id)
        elif action == "add":
            add_list[(ws_id,r_id)].append(u_id)
        else:
            pass

print(delete_list)
print(add_list)

# ロールからの削除を実行
print("===== DELETE users from role =====")
# 対象ワークスペースごとに実行する（が、現在のワークスペースIDと異なるデータは処理しない）
for (ws_id, r_id), u_ids in delete_list.items():
    # 現在のワークスペースがどうか判定
    if str(ws_id) == str(current_workspace_id):
        print(f"対象workspaceId: {ws_id}")
        print(f"対象ロール（PolicyId）: {r_id}")
        print(f"対象ユーザー数: {len(u_ids)}名")
        # API実行
        print("ユーザー削除のレスポンス：")
        response = axycloudapi.delete_role_from_users(AYX_CLOUD_URL, access_token, r_id, u_ids)
        print(response)
    else:
        print(f"workspaceId{ws_id}からの削除は異なるワークスペースのため処理をスキップします。")

# ロールへの追加を実行
print("===== ADD users to role =====")
# 対象ワークスペースごとに実行する（が、現在のワークスペースIDと異なるデータは処理しない）
for (ws_id, r_id), u_ids in add_list.items():
    # 現在のワークスペースがどうか判定
    if str(ws_id) == str(current_workspace_id):
        print(f"対象workspaceId: {ws_id}")
        print(f"対象ロール（PolicyId）: {r_id}")
        print(f"対象ユーザー数: {len(u_ids)}名")
        # API実行
        response = axycloudapi.set_role_to_users(AYX_CLOUD_URL, access_token, r_id, u_ids)
        print(f"ロール割当のレスポンス：{response['name']}")
    else:
        print(f"workspaceId{ws_id}のロール割当は異なるワークスペースのため処理をスキップします。")

