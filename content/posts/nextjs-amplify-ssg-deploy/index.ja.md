---
title: 'Next.jsのSSGをAWS Amplifyにデプロイする方法'
date: 2026-03-08T00:00:00+09:00
draft: false
description: "Next.jsのSSG（Static Site Generation）サイトをAWS Amplifyにデプロイする方法を解説。GitHub連携からamplify.ymlのビルド設定、公開までの手順を初心者向けにまとめています。"
summary: "Next.jsのSSGサイトをAWS Amplifyで公開する方法を解説します。GitHub連携、ビルド設定（amplify.yml）、デプロイまでの手順をわかりやすく紹介します。"
slug: "nextjs-amplify-ssg-deploy"
categories: ["インフラ"]
tags: ["Next.js","AWS","Amplify","SSG","デプロイ"]
showSummary: true
showHero: true
# heroImage: "featured.webp"
---

{{< lead >}}
Next.jsのアプリケーションはVercelでデプロイすることが多いですが、AWS環境で運用したい場合は**AWS Amplify**を利用する方法もあります。  
特に**SSG**（Static Site Generation）のサイトであれば、Amplify Hostingを利用することで簡単にデプロイできます。

この記事では、**Next.jsのSSGサイトをAWS Amplifyにデプロイする方法**を、GitHub連携からビルド設定、公開まで順番に解説します。
{{< /lead >}}

---

## Next.jsをAWS Amplifyにデプロイする全体の流れ

Next.jsのSSGサイトをAmplifyにデプロイする流れは以下の通りです。

1. Next.jsプロジェクトを作成  
2. GitHubにpushする  
3. AWS Amplifyでリポジトリを接続  
4. ビルド設定（amplify.yml）を確認  
5. デプロイ完了  

Amplifyは**Git連携デプロイ**のため、GitHubにpushするだけで自動的にビルドとデプロイが実行されます。

---

## AWS Amplifyとは

AWS Amplifyは、AWSが提供するフロントエンド向けのホスティングサービスです。

主な特徴は以下の通りです。

- GitHubと連携した自動デプロイ  
- CDNによる高速配信  
- HTTPSの自動設定  
- カスタムドメイン対応  

Next.jsの**SSGサイトや静的サイトのホスティング**にも適しています。

---

## Next.jsプロジェクトを作成する

まずはNext.jsのプロジェクトを作成します。

```bash
npx create-next-app amplify-nextjs
````

作成したプロジェクトへ移動します。

```bash
cd amplify-nextjs
```

開発サーバーを起動して動作を確認します。

```bash
npm run dev
```

ブラウザで以下のURLにアクセスすると、Next.jsの初期画面が表示されます。

```text
http://localhost:3000
```

---

## Next.jsをSSGにする方法

Next.jsでは**getStaticProps**を使用することでSSG（静的生成）ができます。

例として、簡単なSSGページを作成します。

```javascript
export async function getStaticProps() {
  return {
    props: {
      message: "Hello Amplify"
    }
  }
}

export default function Home({ message }) {
  return <h1>{message}</h1>
}
```

このようにすると、ビルド時にHTMLが生成される**SSGページ**になります。

---

## GitHubにpushする

AmplifyはGitリポジトリと連携してデプロイするため、GitHubにpushします。

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ユーザー名/リポジトリ名.git
git push origin main
```

---

## AWS AmplifyでNext.jsをデプロイする方法

AWSコンソールからAmplifyを開き、アプリを作成します。

手順は以下です。

1. AWSコンソールを開く
2. Amplifyを選択
3. 「New App」をクリック
4. 「Host web app」を選択
5. GitHubと連携
6. リポジトリを選択

GitHub連携が完了すると、Amplifyが自動でビルド設定を検出します。

---

## amplify.ymlのビルド設定

Next.jsのSSGサイトをデプロイする場合、以下のようなビルド設定になります。

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

この設定により、GitHubにpushすると自動的に以下が実行されます。

1. 依存関係インストール
2. Next.jsビルド
3. CDNへデプロイ

---

## デプロイ完了

ビルドが成功すると、Amplifyが公開URLを発行します。

例

```
https://xxxxx.amplifyapp.com
```

このURLにアクセスすると、Next.jsサイトが公開されています。

また、GitHubに新しくpushすると**自動で再デプロイ**されます。

---

## Next.js Amplifyで使うときの注意点

Next.jsをAmplifyで利用する場合、いくつか注意点があります。

### SSRは追加設定が必要

SSGは問題なく動作しますが、SSR（Server Side Rendering）は追加設定が必要になります。

そのため、**静的サイトとして運用する場合にAmplifyは特に向いています。**

### Nodeバージョン

Next.jsのビルドではNodeバージョンの違いでエラーになる場合があります。
Node18以上を使用するのがおすすめです。

---

## Next.js Amplifyデプロイでよくあるエラー

### buildエラー

原因の多くは以下です。

* Nodeバージョンの違い
* 依存関係のエラー
* amplify.ymlの設定ミス

### 404エラー

Next.jsのルーティング設定によっては、**rewrite設定**が必要になる場合があります。

---

## まとめ

Next.jsのSSGサイトは、AWS Amplifyを利用することで簡単にデプロイできます。

Amplifyの主なメリットは以下です。

* GitHub連携による自動デプロイ
* CDNによる高速配信
* HTTPSの自動設定
* AWS環境で管理できる

Vercel以外の選択肢として、AWSを利用している場合はAmplify Hostingも非常に便利です。
Next.jsのSSGサイトを公開したい場合は、ぜひ試してみてください。

---

## FAQ

### Next.jsはAWS Amplifyで動きますか？

はい。SSGや静的サイトであれば問題なく動作します。

### Next.js SSRはAmplifyで使えますか？

可能ですが、追加設定やAmplify SSR対応機能を利用する必要があります。

### AWS Amplifyは無料ですか？

無料枠がありますが、利用量によっては料金が発生します。

---

## 📘 関連資料

<div class="flex flex-col gap-2 items-start">

{{< button href="[https://docs.aws.amazon.com/amplify/](https://docs.aws.amazon.com/amplify/)" >}}AWS Amplify公式ドキュメント{{< /button >}}

{{< button href="[https://nextjs.org/docs](https://nextjs.org/docs)" >}}Next.js公式ドキュメント{{< /button >}}

</div>
