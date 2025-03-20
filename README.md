# SAM API Dynamo PoC

AWS SAM、API Gateway、Lambda、DynamoDBを使用したAPIのプロトタイプ。

## セットアップと実行方法

このプロジェクトでは、SAM CLIをホストマシンで実行し、DynamoDBのみをDockerコンテナで実行する構成を採用しています。

### 前提条件

- Docker
- AWS SAM CLI
- Python 3.13以上

### 実行手順

```bash
./run_local.sh
```

これにより、ローカルの3000ポートでAPIが起動します。

### APIの使用方法

APIは以下のエンドポイントを提供します：

- GET /users - ユーザー情報を取得

ローカルテスト用に、クエリパラメータでuser_idを指定できます：

```bash
curl "http://localhost:3000/users?user_id=123"
```

## プロジェクト構成

- `template.yaml` - SAMテンプレート
- `src/` - Lambda関数のソースコード
- `scripts/` - セットアップスクリプト
- `tests/` - テストコード
- `compose.yaml` - Dockerコンテナの設定
