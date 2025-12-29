---
title: "🚀 Hugo × Cloudflare Pages で爆速ブログ構築<br>記事作成から公開までの完全ガイド"
date: 2025-12-29T20:50:00+09:00
description: "Hugoでのブログ運用をこれから始める方向けに、効率的な記事作成（Page Bundle）、SEOに強い画像管理、Cloudflare Pagesでの自動デプロイ手順までを完全解説します。"
summary: "「Markdownで書いてGitHubに送るだけ」の爆速ワークフロー。Blowfishテーマを活用したリッチなUI構築と、エンジニアに最適なCloudflareデプロイの秘訣をステップバイステップで解説します。"
categories: ["Web開発", "インフラ"]
tags: ["Hugo", "Cloudflare", "Blowfish", "SSG", "デプロイ", "CI/CD"]
showSummary: true
showHero: true
heroImage: "images/eyecatch/hugo-deploy-hero.webp"
---

{{< lead >}}
静的サイトジェネレーター（SSG）の中でも、圧倒的なビルド速度を誇る **Hugo**。
そこに **Cloudflare Pages** を組み合わせることで、運用コスト0円、かつ爆速でセキュアなブログ環境が手に入ります。
{{< /lead >}}

しかし、いざ始めようとすると「画像はどう管理するのが効率的？」「デプロイ設定のベストプラクティスは？」と迷うポイントも少なくありません。
本記事では、Blowfishテーマを最大限に活かしつつ、**実務で通用する「つまずきゼロ」の公開フロー**を完全網羅しました。

## 1. なぜ「Hugo × Cloudflare Pages」なのか？

個人ブログを構築する手段は様々ですが、この組み合わせには圧倒的なメリットがあります。

- **執筆に集中**: Markdownを書くだけで、複雑なHTML/CSSの調整から解放されます。
- **SEO・パフォーマンス**: 生成されるのは純粋なHTML。最初からPageSpeed Insightsで100点を目指せる基盤があります。
- **Gitによるバージョン管理**: 全ての変更履歴がGitHubに残るため、過去の状態への復元も簡単。
- **完全無料のCI/CD**: `git push` するだけでCloudflareが自動でサイトをビルド・公開。サーバー管理の手間は一切不要です。

---

## 2. 記事作成のベストプラクティス：Page Bundles

Hugoにはいくつかの記事管理方法がありますが、**Page Bundles**形式を強く推奨します。

### 従来の方式 vs Page Bundles
- **従来**: `content/posts/my-post.md` と `static/images/photo.jpg`。画像と記事が離れていて管理しにくい。
- **Page Bundles**: `content/posts/my-post/index.md` と、同じディレクトリ内に画像を配置。**記事ごとに素材を一元管理**できます。

### 記事ディレクトリの作成
```bash
hugo new content posts/my-first-guide/index.ja.md
```

作成されたディレクトリ内に、アイキャッチ画像（`featured.png` など）も一緒に保存しましょう。

---

## 3. Blowfishテーマを使いこなす

当ブログでも採用している **Blowfish** テーマは、Hugoの中でも特にデザイン性と機能性に優れています。

### ショートコードの活用
記事を読みやすくするために、積極的にショートコードを使いましょう。

{{< alert >}}
**おすすめ活用法：**
- `lead`: 導入文を強調
- `alert`: 補足情報や注意喚起
- `button`: 外部リファレンスへの誘導
{{< /alert >}}

### 画像の最適化（Featured Image）
フロントマターで `showHero: true` を設定し、`featured.png` という名前の画像をディレクトリ内に置くだけで、自動的に美しいヒーロー画像（アイキャッチ）が表示されます。

---

## 4. Cloudflare Pages へのデプロイ設定

GitHubへpushした後は、Cloudflare Pages 側で以下の設定を行うだけで公開が完了します。

### ビルド設定の詳細
| 項目 | 設定値 | 理由 |
| :--- | :--- | :--- |
| **Framework preset** | `Hugo` | 標準のプリセットを使用 |
| **Build command** | `hugo --minify` | ファイルを圧縮して高速化 |
| **Build directory** | `public` | 公開用フォルダを指定 |
| **Environment Variable** | `HUGO_VERSION = 0.140.0` | 確実に動作する最新版を指定 |

---

## 5. つまずきがちなポイントと解消法

| 現象 | 原因と解決策 |
| :--- | :--- |
| **画面が真っ白、またはスタイルが崩れる** | `hugo.toml` の `baseURL` が `https://xxx.pages.dev/` など、正しいURLになっているか確認してください。 |
| **画像が表示されない** | 大文字・小文字のミスはないか、Page Bundle の相対パスが正しいかを確認。 |
| **更新が反映されない** | Cloudflareのキャッシュではなく、ビルドログを見てエラーが出ていないかチェック。 |

---

## 6. まとめ：ブログは「資産」になる

Hugoでブログを作ることは、単に情報を発信するだけでなく、**自分だけの技術資産を構築するプロセス**でもあります。
Markdownで書き溜めた記事は将来、別のプラットフォームへ移行する際も汎用性が高く、エンジニアにとって最も「腐りにくい」ストック手法です。

まずは最初の一歩として、今回の手順でHello Worldを公開してみましょう。その一回が、あとの継続を圧倒的に楽にしてくれるはずです。

---

### 📘 関連資料
{{< button href="https://blowfish.page/docs/" target="_blank" >}}
Blowfish 公式ドキュメント
{{< /button >}}
{{< button href="https://developers.cloudflare.com/pages/" target="_blank" >}}
Cloudflare Pages ドキュメント
{{< /button >}}
