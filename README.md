# 本プロジェクトは何？

Alteryx CloudのAPIのサンプルコード置き場です。

# Why Japanese?

一旦日本語で進めます。要望があれば英語版を・・・。
If you want to use this API in English, I will try to translate to English. Please contact with me via Alteryx Community.

# 各pyファイルの説明
- AYX_CloudAPI.py
  - トークンを使ってクレデンシャルを取得するなど共通して利用可能な関数を格納しています
- cloud_api_sample_assign_role.py
  - ロールの一括アサイン用サンプル
- cloud_api_sample_bulk_invite.py
  - ユーザーの一括招待のサンプル

# 使い方
基本的なコンセプトとして、設定情報はPythonと同じフォルダにあるJSONファイルに記載しています。
 - credential.json
   - アクセストークンとリフレッシュトークンを保存 
 - cloud_setting.json
   - クラウドの設定を記載（ayx_cloud_url、refresh_url、oauth_client_id）
