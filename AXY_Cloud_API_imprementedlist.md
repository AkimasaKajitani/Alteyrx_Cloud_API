# AYX_CloudAPI.py 実装状況

本ドキュメントでは、Alteryx Cloud APIに対して、AYX_CloudAPI.py の実装状況を記載しています。

## Billing
本ライブラリでは一部のみ実装済み。

| Lv1 | Lv2 | Method | 説明 | 必要ロール | AYX_CloudAPI |
| --- | --- | --- | --- | --- | --- |
| /billing/v1 | /my/billing-accounts/current | GET | 認証済みユーザーの現在の認証コンテキストにおける請求先アカウントを取得する |  | get_current_billing_accounts |
|  | /usage/export | GET | 集計使用状況の取得 このAPIを使用するには、次のいずれかのロールが必要です: アカウント管理者 | アカウント管理者 |  |

## Identity and Access Management（IAM）
本ライブラリのメイン実装しているAPIです。多くの組織でユーザーマネージメントが必要になりますが、ユーザーマネジメント関連のAPIを本ライブラリでは提供しています。

| Lv1 | Lv2 | Lv3 | Lv4 | Lv5 | Method | 説明 | 必要ロール | AYX_CloudAPI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /iam/v1 | /authorization/roles/{id}/people |  |  |  | PUT | 複数のユーザーにロールを割り当てる | ワークスペース管理者 | set_role_to_users |
|  |  | /{subjectId} |  |  | DELETE | ある特定のユーザーからロールを削除する | ワークスペース管理者 | delete_role_from_user
delete_role_from_users |
|  | /people/{id} |  |  |  | GET | 既存のユーザーの詳細情報を取得する |  |  |
|  | /workspaces | /{id} | /configuration |  | GET | ワークスペースの設定を取得する |  | get_workspace_configuration |
|  |  |  | /invitationLink |  | GET | ある特定のユーザーの招待リンクを取得する |  |  |
|  |  |  | /people |  | GET | 指定されたワークスペースのユーザーを一覧表示する |  | get_workspace_users |
|  |  |  |  | /{personId} | DELETE | ワークスペースからユーザーを削除する。 |  |  |
|  |  |  |  | /batch | POST | ワークスペースにユーザーを一括招待する。 |  | set_invite_users |
|  |  |  |  |  | PATCH | 指定されたワークスペースにユーザーを再度招待します。 |  |  |
|  |  |  |  | /suspend | POST | 指定されたワークスペースのユーザーを停止します。 |  | set_suspend_users |
|  |  |  |  | /unsuspend | POST | 指定されたワークスペースのユーザーの停止を解除します。 |  | set_unsuspend_users |
|  |  |  | /transfer |  | PATCH | Alteryx One アセットをワークスペース内の別のユーザーに譲渡します。 |  | set_transfer_assets |
|  |  | /{workspaceId}/admins |  |  | GET | 指定されたワークスペースの管理者を一覧表示する |  |  |
|  |  | /current |  |  | GET | 現在のワークスペースに関する情報を取得する |  | get_current_workspace |

## Plans
本ライブラリでは未実装。

| Lv1 | Lv2 | Lv3 | Lv4 | Lv5 | Method | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| /plans/v1 | /planEdges |  |  |  | POST | planId と追加のパラメータを指定して、新しいPLANエッジを作成する |
|  | /planNodes |  |  |  | POST | planId と追加のパラメータを指定して、新しいPLANノードを作成する |
|  |  | /{id} |  |  | DELETE | 特定のPLANノードを削除 |
|  |  |  | /runParameters |  | GET | PLANノードの実行パラメータのリストを取得する。  |
|  | /planOverrides |  |  |  | POST | planNodeId と追加のパラメータを指定して、新しいPLANオーバーライドを作成する |
|  |  | /{id} |  |  | PUT | 特定のプランのオーバーライド構成を更新する |
|  | /plans |  |  |  | GET | クエリ パラメータを使用して結果をフィルター処理し、既存のすべてのプランとその詳細を取得する |
|  |  |  |  |  | POST | プランの名前とその他のオプション パラメータを定義して、新しいプランを作成する |
|  |  | /{id} |  |  | PATCH | 名前や説明など、特定のプランのプロパティを更新する |
|  |  |  |  |  | DELETE | 特定のプランを削除し、それに関連付けられたスケジュールも削除する |
|  |  |  | /full |  | GET | すべてのノード、タスク、エッジを含む完全なプランを取得する |
|  |  |  | /package |  | GET | 指定されたプランの定義を含むパッケージを取得する。  |
|  |  |  | /permissions |  | GET | プランを共有しているユーザーのリストを取得する。 |
|  |  |  |  |  | POST | 他のユーザーとプランを共有し、特定のロールとポリシーを割り当てる。 |
|  |  |  |  | /{subjectId} | DELETE | 特定のプランから権限を削除する |
|  |  |  | /run |  | POST | 特定のプランを実行する。必要に応じて新しいスナップショットが作成される。 |
|  |  |  | /runParameters |  | GET | 特定のプランの実行パラメータのリストを、プランノードごとにグループ化して取得する。  |
|  |  |  | /schedules |  | GET | 特定のプランに設定されているすべてのスケジュールを取得する。 |
|  |  | /count |  |  | GET | 指定されたクエリ パラメータに基づいて、既存のプランの合計数を取得する |
|  |  | /package |  |  | POST | 提供されたパッケージからプランと関連フローをインポートする。 |

## Scheduling
本ライブラリでは未実装。

| Lv1 | Lv2 | Lv3 | Lv4 | Method | 説明 |
| --- | --- | --- | --- | --- | --- |
| /scheduling/v1 | /schedules |  |  | GET | 現在のユーザーが所有する詳細とともにスケジュールのリストを管理および取得する |
|  |  |  |  | POST | スケジュールの名前、トリガー、タスクを定義して、新しいスケジュールを作成する |
|  |  | /{id} |  | GET | 特定のスケジュールの詳細を取得する |
|  |  |  |  | PUT | 特定のスケジュールの詳細を更新する |
|  |  |  |  | DELETE | 特定のスケジュールを削除する |
|  |  |  | /disable | POST | 特定のスケジュールを無効にする |
|  |  |  | /enable | POST | 現在無効になっているスケジュールを有効にする |
|  |  | /count |  | GET | 現在のユーザーが所有するスケジュールの合計数を取得する |

## Trifacta Classic
レガシープロダクトのため未実装（実装予定なし）
