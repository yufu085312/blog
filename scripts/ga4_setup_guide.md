# GA4 API連携セットアップガイド

Pythonスクリプト (`scripts/update_popular_articles.py`) から GA4 の閲覧数データを取得するための手順を説明します。

---

## ステップ 1: Google Cloud プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. **Google Analytics Data API** を有効にします。
    - メニューの「APIとサービス」 > 「ライブラリ」から "Google Analytics Data API" を検索し、「有効にする」をクリックします。

---

## ステップ 2: サービスアカウントの作成と鍵の取得

1. 「APIとサービス」 > 「認証情報」をクリックします。
2. 「認証情報を作成」 > 「サービスアカウント」をクリックします。
3. アカウント名（例: `ga4-popular-articles`）を入力し、作成します。ロールの選択は空のままでも構いません。
4. 作成されたサービスアカウントのメールアドレス（例: `ga4-popular-articles@project-id.iam.gserviceaccount.com`）をコピーしておきます。
5. サービスアカウントの詳細画面の「キー」タブをクリックします。
6. 「鍵を追加」 > 「新しい鍵を作成」をクリックし、**JSON** 形式を選択して「作成」をクリックします。
7. ダウンロードされた JSON ファイルを保存します（これを `ga4-creds.json` とリネームしておきます）。

---

## ステップ 3: GA4 プロパティへのユーザー追加

1. [Google Analytics (GA4)](https://analytics.google.com/) にアクセスします。
2. 左下の「管理」をクリックします。
3. プロパティ列の「プロパティのアクセス管理」をクリックします。
4. 右上の「＋」ボタンをクリックし、「ユーザーを追加」を選択します。
5. **ステップ 2 でコピーしたサービスアカウントのメールアドレス**を入力します。
6. ロールは「閲覧者」で十分です。「追加」をクリックします。

---

## ステップ 4: スクリプトの実行準備

### 1. 仮想環境の作成とライブラリのインストール
ターミナルで以下を実行します：
```bash
# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 仮想環境内でライブラリをインストール
./venv/bin/pip install google-analytics-data
```

### 2. 環境変数の設定
ダウンロードした JSON 鍵ファイルをプロジェクトルートに配置した場合：

```bash
# 認証情報の指定
export GOOGLE_APPLICATION_CREDENTIALS="ga4-creds.json"

# GA4 プロパティIDの指定
export GA4_PROPERTY_ID="あなたのプロパティID"
```

### 3. スクリプトの実行
仮想環境内のPythonを使用して実行します。
```bash
./venv/bin/python scripts/update_popular_articles.py
```

実行に成功すると、`data/popular_articles.json` が最新の閲覧数データで更新されます。
