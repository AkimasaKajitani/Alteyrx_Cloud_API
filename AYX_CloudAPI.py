import urllib.parse
import urllib.request
import json
import time

# ============= 使い方 =============================================
# 外部JSONファイルにCloudで取得したOAuth2.0 APIトークンのアクセストークン、リフレッシュトークンを貼り付けて保存
USER_AGENT = "AYX_CloudAPI by AK"
SLEEP_VALUE = 0.2

# ============= 関数 =============================================
# JSONファイルの読み込み
def _read_tokens(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            return access_token, refresh_token
    except FileNotFoundError:
        print(f"{json_file}が見つかりません")
        return None, None
    except json.JSONDecodeError:
        print("JSONの読み込みに失敗しました")
        return None, None

# JSONファイルへのトークンの書き込み
def _write_tokens(json_file, access_token, refresh_token):
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("トークンを保存しました")

# トークンの更新
def _refresh_tokens(refresh_token, refresh_url, oauth2_client_id):
  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }
  body = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': oauth2_client_id
  }
 
  # URL encode the body for the refresh request
  encoded_body = urllib.parse.urlencode(body).encode()

  # Make the refresh request
  request = urllib.request.Request(refresh_url, data=encoded_body, method='POST')
  with urllib.request.urlopen(request) as response:
    return json.load(response)

# ========== 外部から呼び出す用関数 ==========
# トークン更新
def update_tokens(refresh_url, oauth2_client_id, json_file):
    # JSONファイルから読み込み
    access_token_json, refresh_token_json = _read_tokens(json_file)
    # トークンを更新
    new_tokens = _refresh_tokens(refresh_token_json, refresh_url, oauth2_client_id)
    # 更新されたトークンを保存
    _write_tokens(json_file, new_tokens['access_token'], new_tokens['refresh_token'])

    return new_tokens['access_token']

# Cloud設定読み込み
def load_cloud_setting(json_file):
    # JSONファイルから読み込み
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            ayx_cloud_url = data.get('ayx_cloud_url')
            refresh_url = data.get('refresh_url')
            oauth_client_id = data.get('oauth_client_id')

            print("クラウド設定を読み込みました")
            print(f"ayx_cloud_url : {ayx_cloud_url}\nrefresh_url : {refresh_url}\noauth_client_id : {oauth_client_id}")
            return ayx_cloud_url, refresh_url, oauth_client_id
    except FileNotFoundError:
        print(f"{json_file}が見つかりません")
        return None, None, None
    except json.JSONDecodeError:
        print("JSONの読み込みに失敗しました")
        return None, None, None

# 現在のワークスペース情報を取得
def get_current_workspace(aac_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
    }
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/current', headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# 請求情報取得
def get_current_billing_accounts(aac_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
    }
    request = urllib.request.Request(f'{aac_url}/billing/v1/my/billing-accounts/current', headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# 指定したワークスペースのユーザー一覧を取得
def get_workspace_users(aac_url, access_token, workspaceid, offset, limit):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
    }
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/people?includePrivileges=true&offset={offset}&limit={limit}', headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# 指定したワークスペースのユーザー一覧（全数）を取得
def get_workspace_users_all(aac_url, access_token, workspaceid):
    # ワークスペース全体のユーザー数を取得
    current_workspace_info = get_current_workspace(aac_url, access_token)
    totalPeople = current_workspace_info['workspace_member_count']

    all_data = []
    limit = 50
    for offset in range(0, totalPeople, limit):
        data = get_workspace_users(aac_url, access_token, workspaceid, offset, limit)
        all_data.extend(data['data'])
        time.sleep(SLEEP_VALUE)
    return all_data

# 指定したワークスペースの設定情報を取得
def get_workspace_configuration(aac_url, access_token, workspaceid):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
    }
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/configuration', headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


# 指定したロールにユーザーをセット
def set_role_to_users(aac_url, access_token, policyid, users):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data_bytes = json.dumps(users).encode('utf-8')
    request = urllib.request.Request(f'{aac_url}/iam/v1/authorization/roles/{policyid}/people', headers=headers, data=data_bytes, method='PUT')
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# 指定したロールからユーザーを削除
def delete_role_from_user(aac_url, access_token, policyid, user):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
    }
    request = urllib.request.Request(f'{aac_url}/iam/v1/authorization/roles/{policyid}/people/{user}', headers=headers, method='DELETE')
    with urllib.request.urlopen(request) as response:
        if response.status == 200:
            return "Success"
        else:
            return response.status

# 指定したロールから一括でユーザーを削除
def delete_role_from_users(aac_url, access_token, policyid, users):
    results = []
    for user in users:
        response = delete_role_from_user(aac_url, access_token, policyid, user)
        results.append({
            'user':user,
            'response':response
        })
        time.sleep(SLEEP_VALUE)
    return results

# 指定したユーザーをサスペンドする
def set_suspend_users(aac_url, access_token, workspaceid, users):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "personIds": users
    }
    data_bytes = json.dumps(data).encode('utf-8')
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/people/suspend', headers=headers, data=data_bytes)
    with urllib.request.urlopen(request) as response:
        if response.status == 200:
            return "Success"
        else:
            return response.status

# 指定したユーザーをサスペンドから復帰させる
def set_unsuspend_users(aac_url, access_token, workspaceid, users):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "personIds": users
    }
    data_bytes = json.dumps(data).encode('utf-8')
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/people/unsuspend', headers=headers, data=data_bytes)
    with urllib.request.urlopen(request) as response:
        if response.status == 200:
            return "Success"
        else:
            return response.status

# 指定したユーザー(email)を招待する
def set_invite_users(aac_url, access_token, workspaceid, emails):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "AYX_CloudAPI by AK",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    requestBody = {
        "emails": emails
    }
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/people/batch', headers=headers, data=json.dumps(requestBody).encode('utf-8'), method='POST')
    with urllib.request.urlopen(request) as response:
        return json.load(response)

# 指定したユーザー(email)を招待する
def set_transfer_assets(aac_url, access_token, workspaceid, from_user, to_user):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "AYX_CloudAPI by AK",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    requestBody = {
        "fromPersonId": from_user,
        "toPersonId": to_user
    }
    request = urllib.request.Request(f'{aac_url}/iam/v1/workspaces/{workspaceid}/transfer', headers=headers, data=json.dumps(requestBody).encode('utf-8'), method='PATCH')
    with urllib.request.urlopen(request) as response:
        if response.status == 204:
            return "Success"
        else:
            return response.status


# ============= For Debug =============================================
if __name__ == "__main__":

    # 固定値
    JSON_FILE_PATH = "credential.json"
    CLOUD_SETTING_JSON = "cloud_setting.json"

    # クラウド設定の読み込み
    AYX_CLOUD_URL, REFRESH_URL, OAUTH_CLIENT_ID = load_cloud_setting(CLOUD_SETTING_JSON)

    # アクセストークン更新
    access_token_json, refresh_token_json = _read_tokens(JSON_FILE_PATH)

    new_tokens = _refresh_tokens(refresh_token_json,REFRESH_URL,OAUTH_CLIENT_ID)
    # 更新されたトークンを保存
    _write_tokens(JSON_FILE_PATH,new_tokens['access_token'],new_tokens['refresh_token'])

    print("New Access Token:", new_tokens['access_token'])
    print("New Refresh Token:", new_tokens['refresh_token'])

    # 請求情報取得
    billinginfo = get_current_billing_accounts(AYX_CLOUD_URL, new_tokens['access_token'])

    print("請求情報：")
    print(billinginfo)
    print("契約に紐づくワークスペースID：")
    print(billinginfo['data']['workspaces']) # ワークスペースID取得

    # ワークスペースID取得
    workspaceinfo = get_current_workspace(AYX_CLOUD_URL, new_tokens['access_token'])

    print("ワークスペースID：")
    print(workspaceinfo)
    print(workspaceinfo['id'])

    # ユーザー一覧取得
    workspace_users = get_workspace_users_all(AYX_CLOUD_URL, new_tokens['access_token'], workspaceinfo['id'])
    print("ユーザー一覧：")
    print(workspace_users)

    # ワークスペース設定情報取得
    workspaceconfiguration = get_workspace_configuration(AYX_CLOUD_URL, new_tokens['access_token'], workspaceinfo['id'])

    print("ワークスペース設定情報：")
    print(workspaceconfiguration)

    # ロールにユーザーを割り当てる
    #polycyid = -1 # ロール
    #users= [-1]
    #response = set_role_to_users(AYX_CLOUD_URL, new_tokens['access_token'], polycyid, users)
    #print("ユーザー割当のレスポンス：")
    #print(response)

    # ロールからユーザーを削除
    #polycyid = -1 # ロール
    #user= -1
    #response = delete_role_from_user(AYX_CLOUD_URL, new_tokens['access_token'], polycyid, user)
    #print("ユーザー削除のレスポンス：")
    #print(response)

    # ロールから複数ユーザーを削除
    #polycyid = -1 # ロール
    #user= [-1]
    #response = delete_role_from_users(AYX_CLOUD_URL, new_tokens['access_token'], polycyid, users)
    #print("ユーザー削除のレスポンス：")
    #print(response)

    # 指定したユーザーをサスペンドする
    #users= [-1,-2]
    #response = set_suspend_users(AYX_CLOUD_URL, new_tokens['access_token'], workspaceinfo['id'], users)
    #print("ユーザーサスペンドのレスポンス：")
    #print(response)

    # 指定したユーザーをサスペンドから復帰させる
    #users= [-1,-2]
    #response = set_unsuspend_users(AYX_CLOUD_URL, new_tokens['access_token'], workspaceinfo['id'], users)
    #print("ユーザーサスペンド解除のレスポンス：")
    #print(response)

    # 指定したユーザー(email)を招待する
    #emails = ["thoughtspot@kcme.jp"]
    #response = set_invite_users(AYX_CLOUD_URL, new_tokens['access_token'], workspaceinfo['id'], emails)
    #print("ユーザー招待のレスポンス：")
    #print(response)

    # 指定したユーザーのアセットを別のユーザーに割り当てる
    #from_user = -1
    #to_user = -2
    #response = set_transfer_assets(AYX_CLOUD_URL, new_tokens['access_token'], workspaceinfo['id'], from_user, to_user)
    #print("所有権転送のレスポンス：")
    #print(response)


else:
        pass
