# エンジニア技術ブログ (yu-fu.site)

Hugo と Blowfish テーマを使用した個人ブログプロジェクトです。
GitHub Actions / Cloudflare Pages を通じて自動デプロイされています。

## 🛠 1. 環境構築

本プロジェクトは Hugo を使用しています。

### 必要ツール
- [Hugo Extended](https://gohugo.io/installation/) (バージョン 0.140.0 以上推奨)
- [Git](https://git-scm.com/)

### セットアップ
```bash
# リポジトリのクローン
git clone https://github.com/yufu085312/blog.git
cd blog

# サブモジュール（テーマ）の更新
git submodule update --init --recursive
```

## 🚀 2. 起動・プレビュー方法

ローカル環境でサイトを確認するには以下のコマンドを実行します。

```bash
# 下書き（Draft）を含めてプレビュー
hugo server -D
```

- 実行後、ブラウザで [http://localhost:1313/](http://localhost:1313/) にアクセスしてください。
- ファイルを保存するとブラウザが自動的に更新されます。

## ✍️ 3. 記事の作成方法

記事は管理しやすい **Page Bundle** 形式で作成します。

```bash
# 新しい記事フォルダとファイルを作成
hugo new content posts/[記事タイトル]/index.ja.md
```

### 執筆のルール
1.  **画像の配置**: 作成されたフォルダ内に直接画像（`featured.png` など）を置きます。
2.  **フロントマターの設定**:
    - `draft: true` : 書きかけの時は true、公開する時は false にします。
    - `showHero: true` : 記事のトップに画像を表示します。
    - `summary`: 一覧ページに表示される紹介文を記述します。

## 🚢 4. デプロイ

`main` ブランチにプッシュすると、Cloudflare Pages により自動的にビルドとデプロイが行われます。

```bash
git add .
git commit -m "feat: 〇〇の記事を追加"
git push origin main
```
