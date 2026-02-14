---
title: "Next.js 環境構築の完全手順書｜最初にやるべき設定まとめ"
date: 2026-02-14T15:30:00+09:00
draft: false
description: "Next.jsの環境構築で最初にやるべき設定を、create-next-appから初期ディレクトリ構成、TypeScript・Lint・Git設定まで実務視点でまとめた完全手順書です。"
summary: "create-next-appで終わらせない。実務でそのまま使える Next.js 環境構築の手順を、初期設定・設計の考え方込みで解説します。"
slug: "nextjs-environment-setup-guide"
categories: ["フロントエンド", "Next.js"]
tags: ["Next.js", "React", "環境構築", "TypeScript", "実務"]
showSummary: true
showHero: true
---

{{< lead >}}
Next.jsの環境構築は、  
**「とりあえず create-next-app して動いたらOK」**  
で終わらせてしまうと、あとから高確率で詰みます。

- Lintが途中から地獄になる  
- ディレクトリ構成がぐちゃぐちゃになる  
- チーム開発でルールが合わず事故る  

私は実務で、**「最初に決めなかったこと」が原因の修正・やり直し**を何度も経験してきました。

この記事では、  
**実務でそのまま使える Next.js の環境構築手順**を、  
「なぜその設定を最初にやるのか」という理由付きでまとめます。
 
**Next.js をこれから実務・個人開発で使い始めるエンジニア向け**に、  
「あとから後悔しない初期環境」を作ることを目的としています。
{{< /lead >}}

---

## 1. Next.js 環境構築の全体像

まず、この記事で構築する環境のゴールを明確にします。

### 本記事のゴール

- Next.js（App Router）
- TypeScript
- ESLint（初期から有効）
- 実務を想定したディレクトリ構成
- Git管理まで完了した状態

> **すぐ開発を始められる安全な初期状態**を作るのが目的です。

---

## 2. Node.js の準備（最重要）

### 2.1 Node.js の推奨バージョン

Next.js は **Node.js LTS** を使うのが基本です。

```bash
node -v
```

* 推奨：LTS（例：18 / 20 系）
* 避ける：古すぎるバージョン、開発版

Node のバージョン違いは、
**環境構築トラブルの原因 No.1** です。

> 補足：
> 実務では、Node.js のバージョンを `.nvmrc` や `.node-version` で固定することが一般的です。
> チーム開発では「動く / 動かない」の差分を防ぐため、バージョン固定を強く推奨します。

---

## 3. create-next-app でプロジェクト作成

```bash
npx create-next-app@latest my-app
cd my-app
```

### 3.1 質問項目のおすすめ設定

実務前提なら、以下がおすすめです。

* TypeScript → **Yes**
* ESLint → **Yes**
* App Router → **Yes**
* src/ directory → **Yes**
* import alias → **Yes**

#### なぜこの設定か？

* **TypeScript**：後から入れると修正コストが高い
* **ESLint**：最初からルールを固定するため
* **App Router**：現在のNext.js標準
* **src/**：構造を整理しやすい
* **alias**：import地獄を防ぐ

> create-next-app で生成される `.gitignore` は、そのまま使って問題ありません。
> 独自で追加する場合は、`.env.local` を必ず除外しましょう。

---

## 4. 初期ディレクトリ構成を理解する

作成直後の構成は、だいたい以下のようになります。

```txt
src/
├─ app/
│  ├─ layout.tsx
│  ├─ page.tsx
│  └─ globals.css
├─ components/
├─ lib/
└─ styles/
```

### 4.1 触っていい場所・注意が必要な場所

* `app/`：ルーティングの中心（慎重に）
* `components/`：UI部品
* `lib/`：API通信・ユーティリティ
* `public/`：画像・静的ファイル

> **最初に役割を決めないと、後から整理できなくなります。**

---

## 5. ESLint を「最初に」整える理由

### なぜ後回しにしてはいけないのか

* 途中からルールを入れると警告が大量発生
* チーム内で書き方がバラバラになる
* 修正コストが一気に跳ね上がる

create-next-app で入った ESLint は、
**最低限でも十分に価値があります。**

```bash
npm run lint
```

まずは **エラーが出ない状態を保つ** ことを最優先にしましょう。

---

## 6. 開発サーバー起動と動作確認

```bash
npm run dev
```

* [http://localhost:3000](http://localhost:3000) にアクセス
* 初期画面が表示されればOK

### よくあるエラー

* Nodeバージョン不一致
* ポート競合
* npm install 忘れ

---

## 7. Git 初期化（ここまでが環境構築）

```bash
git init
git add .
git commit -m "init: create next.js app"
```

### なぜここまでやるのか

* 環境構築も **履歴として残す**
* 後から戻せる状態を作る
* 実務では「最初のcommit」が超重要

> **Git管理まで含めて、環境構築は完了**です。

---

## 8. 実務でよくあるハマりポイント

* Node / npm / pnpm が混在
* App Router の概念を理解せずに実装
* Lintを無視して進める
* 初期設計なしでcomponentsが肥大化

どれも、**最初に整えていれば防げる問題**です。

---

### 環境構築が終わったら次にやること

環境構築が終わったら、次にやるべきことは以下です。

1. ディレクトリ設計を固める
2. コンポーネント分割ルールを決める
3. API / データ取得方法を整理する

※これらは別記事で詳しく解説予定です。

---

## まとめ

Next.js の環境構築は、
**「動いたら終わり」ではありません。**

* 後から直すとコストが跳ね上がる
* 初期設計が、そのままプロジェクト寿命を決める
* 最初の1時間が、数ヶ月後の楽さを作る

この記事の状態をベースにすれば、
**安心して開発を始められる Next.js 環境**になります。

---

## 📘 関連リンク

<div class="flex flex-col gap-2 items-start">
{{< button href="https://nextjsjp.org/">}}
Next.js 公式ドキュメント
{{< /button >}}
{{< button href="/posts/nextjs-15-setup-guide/" >}}
Next.js 15 の環境構築手順と徹底解説
{{< /button >}}
</div>
