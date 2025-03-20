#!/bin/bash
set -euo pipefail

# 依存関係を直接srcディレクトリにインストール
echo "依存関係をインストール中..."
pip install -t src/ boto3 aws-lambda-powertools

# DynamoDBとセットアップコンテナを起動
echo "DynamoDBとセットアップコンテナを起動中..."
docker compose up --build -d

# コンテナの起動を待機
echo "コンテナの起動を待機中..."
sleep 5

# SAM CLIを使用してAPIを起動
echo "SAM CLIを使用してAPIを起動中..."
uv run sam local start-api --env-vars .env.json

# 終了時にコンテナを停止
trap 'echo "コンテナを停止中..."; docker compose down' EXIT
