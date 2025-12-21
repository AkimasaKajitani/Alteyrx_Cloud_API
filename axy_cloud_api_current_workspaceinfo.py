import axycloudapi
import pandas as pd
import yaml
import os
import sys

# ============== このサンプルは何ですか？ ================
# 取得したOAuth2.0 APIトークンに応じたワークスペース環境の基本情報を取得するコードです
# 1. クラウド設定とトークンをそれぞれ同じフォルダ内のJSONファイルに記載する
# 2. 本プログラムを実行
# トークン：Cloudの[ユーザー設定]-[OAuth 2.0 APIトークン]から取得し、credential.jsonに記載する
# クラウド設定：cloud_setting.jsonに記載する
# ======================================================


# その他設定(固定値)
JSON_FILE_PATH = "credential.json"
CLOUD_SETTING_JSON = "cloud_setting.json"
SETTING_YAML = "axy_cloud_api_current_workspaceinfo_config.yaml"

# ============== 関数 ==============
# 入れ子になっているJSONを展開する（別テーブルとして保存する）
def getDetaillist(df, columnName):
    rows = []
    for person in df:
        if columnName not in person or person[columnName] is None:
            continue
        
        id = person.get('id', 'N/A')
        for item in person[columnName]:
                row = {'id': id}
                # 全てのデータをコピーし、operationsだけ上書きする
                row.update(item) 
                if 'operations' in row:
                    row['operations'] = ", ".join(row['operations'])
                
                rows.append(row)
    return pd.DataFrame(rows)

# ============== メインコード ==============
# クラウド設定の読み込み
AYX_CLOUD_URL, REFRESH_URL, OAUTH_CLIENT_ID = axycloudapi.load_cloud_setting(CLOUD_SETTING_JSON)

# 設定ファイル（YAML）の読み込み
if os.path.exists(SETTING_YAML):
    with open(SETTING_YAML, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
else:
    # 設定ファイルがなければ処理をストップ
     print(f"設定ファイル「{SETTING_YAML}」がありません。")
     sys.exit(1)

# アクセストークン取得（と更新）
access_token = axycloudapi.update_tokens(REFRESH_URL, OAUTH_CLIENT_ID, JSON_FILE_PATH)

# 請求情報保存
billinginfo = axycloudapi.get_current_billing_accounts(AYX_CLOUD_URL, access_token)

df_billinginfo = pd.DataFrame(billinginfo['data'])
df_billinginfo.to_csv("billing_account.csv", index=False, encoding="utf-8-sig")
print(df_billinginfo)

# ワークスペース情報取得
workspaceinfo = axycloudapi.get_current_workspace(AYX_CLOUD_URL, access_token)
df_workspaceinfo = pd.DataFrame(workspaceinfo)
df_workspaceinfo.to_csv(f"workspaceinfo_{workspaceinfo['id']}.csv", index=False, encoding="utf-8-sig")
print(df_workspaceinfo)

# ユーザー一覧取得
workspace_users = axycloudapi.get_workspace_users_all(AYX_CLOUD_URL, access_token, workspaceinfo['id'])

# Fullバージョンはtsvで保存
df_workspace_users_full = pd.DataFrame(workspace_users)
df_workspace_users_full.to_csv(f"workspaceusers_{workspaceinfo['id']}_full.tsv", index=False, encoding="utf-8-sig", sep='\t')

# メイン項目を保存
target_columns = config['workspaceinfo']['columns'] # YAMLファイルに設定した項目のみ出力する
df_workspace_users = pd.DataFrame(workspace_users, columns=target_columns)
print(df_workspace_users)
df_workspace_users.to_csv(f"workspaceusers_{workspaceinfo['id']}.csv", index=False, encoding="utf-8-sig")

## 入れ子になっているものは個別に保存
# maximalPrivileges
df_maximalPrivileges = getDetaillist(workspace_users,'maximalPrivileges')
df_maximalPrivileges.to_csv(f"workspaceusers_{workspaceinfo['id']}_maximalPrivileges.csv", index=False, encoding="utf-8-sig")
# peopleworkspaces
df_peopleworkspaces = getDetaillist(workspace_users,'peopleworkspaces')
df_peopleworkspaces.to_csv(f"workspaceusers_{workspaceinfo['id']}_peopleworkspaces.csv", index=False, encoding="utf-8-sig")
# authorizationRoles
df_authorizationRoles = getDetaillist(workspace_users,'authorizationRoles')
df_authorizationRoles.to_csv(f"workspaceusers_{workspaceinfo['id']}_authorizationRoles.csv", index=False, encoding="utf-8-sig")
df_rolelist_dropdupli = df_authorizationRoles.drop_duplicates(subset=['policyId','name','tag','workspaceId'],ignore_index=True)
df_rolelist = df_rolelist_dropdupli[['policyId','name','tag','workspaceId']]

print(df_authorizationRoles)

# まとめ
print(f"あなたの環境：{billinginfo['data']['name']}")
print(f"ワークスペースID：{workspaceinfo['id']}")
print(f"ワークスペース名：{workspaceinfo['name']}")
print(f"ワークスペース{workspaceinfo['id']}の割り当て済みRole Policyリスト：")
print(df_rolelist)

