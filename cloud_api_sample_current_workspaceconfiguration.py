import AYX_CloudAPI
import pandas as pd
import ast

# ============== このサンプルは何ですか？ ================
# 取得したOAuth2.0 APIトークンに応じたワークスペース環境の設定情報を取得するコードです
# 1. クラウド設定とトークンをそれぞれ同じフォルダ内のJSONファイルに記載する
# 2. 本プログラムを実行
# トークン：Cloudの[ユーザー設定]-[OAuth 2.0 APIトークン]から取得し、credential.jsonに記載する
# クラウド設定：cloud_setting.jsonに記載する
# ======================================================


# その他設定(固定値)
JSON_FILE_PATH = "credential.json"
CLOUD_SETTING_JSON = "cloud_setting.json"

# ============== メインコード ==============
# クラウド設定の読み込み
AYX_CLOUD_URL, REFRESH_URL, OAUTH_CLIENT_ID = AYX_CloudAPI.load_cloud_setting(CLOUD_SETTING_JSON)

# アクセストークン取得（と更新）
access_token = AYX_CloudAPI.update_tokens(REFRESH_URL, OAUTH_CLIENT_ID, JSON_FILE_PATH)

# ワークスペース情報取得
## 現在のワークスペースIDを取得
current_workspace_info = AYX_CloudAPI.get_current_workspace(AYX_CLOUD_URL, access_token)

## 設定を取得する
workspaceconfiguration = AYX_CloudAPI.get_workspace_configuration(AYX_CLOUD_URL, access_token, current_workspace_info['id'])
df_workspaceconfiguration = pd.json_normalize(workspaceconfiguration)
print(df_workspaceconfiguration)

## CSV保存
df_workspaceconfiguration.to_csv(f"workspaceconfiguration_{current_workspace_info['id']}.csv", index=False, encoding="utf-8-sig")
