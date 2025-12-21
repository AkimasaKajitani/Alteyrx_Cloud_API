# 本プロジェクトは何？

Alteryx CloudのAPIのサンプルコード置き場です。Alteryx非公認のプロジェクトですので、ご利用は自己責任でお願いします。本プロジェクトの成果物を利用し、何らかの損害を被ったとしても当方は一切の責任を持ちません。


# Why Japanese?

一旦日本語で進めます。要望があれば英語版を・・・。
If you want to use this API in English, I will try to translate to English. Please contact with me via Alteryx Community.


# 各ファイルの説明
## pyファイル
- axycloudapi.py
  - Alteryx Cloud APIを使うためのサポートライブラリ。APIを使うにあたり共通化すべき機能（認証関係）や、実際によく使われそうな機能を実装。実装状況は[こちら](https://github.com/AkimasaKajitani/Alteyrx_Cloud_API/blob/main/AXY_Cloud_API_imprementedlist.md)です。
- axy_cloud_api_current_workspaceinfo.py
  - OAuth2.0クレデンシャルを取得したワークスペースの基本情報を取得するサンプル
- axy_cloud_api_current_workspaceconfiguration.py
  - OAuth2.0クレデンシャルを取得したワークスペースの基本設定を取得するサンプル
- cloud_api_sample_assign_role.py
  - ロールの一括アサイン用サンプル
- cloud_api_sample_bulk_invite.py
  - ユーザーの一括招待のサンプル


## JSONファイル
- cloud_setting_format.json
  - クラウド設定のフォーマットファイル。実際に利用する場合は、ファイル名から「_format」を削除し「cloud_setting.json」というファイル名でお使いください（もしくはコード側をファイル名に合わせてください）
- credential_format.json
  - クレデンシャル（アクセストークン、リフレッシュトークン）の設定用ファイルフォーマット。実際に利用する場合は、ファイル名から「_format」を削除し「credential.json」というファイル名でお使いください（もしくはコード側をファイル名に合わせてください）

    
## YAMLファイル
- axy_cloud_api_current_workspaceinfo_config.yaml
  - axy_cloud_api_current_workspaceinfo.py 用の設定ファイル


# 使い方
基本的なコンセプトとして、設定情報とコードは分離しています。設定情報の保存先としてはPythonと同じフォルダにあるJSONファイルとしています。そのため、このJSONさえ変更すれば動作する作りとなっています。
 - credential.json
   - アクセストークンとリフレッシュトークンを保存 
 - cloud_setting.json
   - クラウドの設定を記載（ayx_cloud_url、refresh_url、oauth_client_id）
いずれの設定も、Alteryx Cloud Platform上で設定情報を取得します。Alteryx Cloud Platformにログインし、[ユーザー設定]-[OAuth 2.0 APIトークン]にてトークンを作成し、トークン情報をcredential.jsonに記載します。同じくクラウド設定も取得できます。

それぞれのサンプルコードで必要になる設定は、それぞれのコードの説明をお読みください。

## axy_cloud_api_current_workspaceinfo.py
Alteryx CloudのAPIを使うために必要な情報などを取得するためのサンプルプログラムを作成しました。このコードは以下のことが実行可能です。
- ユーザーリストの取得
- ワークスペースの基本情報の取得（契約名、ワークスペースID、ワークスペース名）
- ワークスペース内でユーザーに割り当てられているロールのPolicyIdのリスト
- 以下のCSVの取得
  - billing_account.csv
  - workspaceinfo_[ワークスペースID].csv
  - workspaceusers_[ワークスペースID]_full.tsv　※全データ
  - workspaceusers_[ワークスペースID].csv　※主要項目のみのユーザーリスト
  - workspaceusers_[ワークスペースID]_authorizationRoles.csv　※Roleのポリシー
  - workspaceusers_[ワークスペースID]_maximalPrivileges.csv　※maximalPrivilegesを展開したデータ
  - workspaceusers_[ワークスペースID]_peopleworkspaces.csv　※peopleworkspacesを展開したデータ
- 以下のモジュールのインストールが必要です
  - pandas
  - pyyaml

 
