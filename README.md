# 本プロジェクトは何？

Alteryx CloudのAPIのサンプルコード置き場です。

# Why Japanese?

一旦日本語で進めます。要望があれば英語版を・・・。
If you want to use this API in English, I will try to translate to English. Please contact with me via Alteryx Community.

# 各ファイルの説明
## pyファイル
- AYX_CloudAPI.py
  - トークンを使ってクレデンシャルを取得するなど共通して利用可能な関数を格納しています
- cloud_api_sample_assign_role.py
  - ロールの一括アサイン用サンプル
- cloud_api_sample_bulk_invite.py
  - ユーザーの一括招待のサンプル

## JSONファイル
- cloud_setting_format.json
  - クラウド設定のフォーマットファイル。実際に利用する場合は、ファイル名から「_format」を削除し「cloud_setting.json」というファイル名でお使いください（もしくはコード側をファイル名に合わせてください）
- credential_format.json
  - クレデンシャル（アクセストークン、リフレッシュトークン）の設定用ファイルフォーマット。実際に利用する場合は、ファイル名から「_format」を削除し「credential.json」というファイル名でお使いください（もしくはコード側をファイル名に合わせてください）

# 使い方
基本的なコンセプトとして、設定情報とコードは分離しています。設定情報の保存先としてはPythonと同じフォルダにあるJSONファイルとしています。そのため、このJSONさえ変更すれば動作する作りとなっています。
 - credential.json
   - アクセストークンとリフレッシュトークンを保存 
 - cloud_setting.json
   - クラウドの設定を記載（ayx_cloud_url、refresh_url、oauth_client_id）
いずれの設定も、Alteryx Cloud Platform上で設定情報を取得します。Alteryx Cloud Platformにログインし、[ユーザー設定]-[OAuth 2.0 APIトークン]にてトークンを作成し、トークン情報をcredential.jsonに記載します。同じくクラウド設定も取得できます。

それぞれのサンプルコードで必要になる設定は、それぞれのコードの説明をお読みください。
