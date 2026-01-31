---
title: 'Next.jsで動画は再生されるのにモバイルだけエラーが出る理由'
date: 2026-01-31T16:52:42+09:00
draft: false
description: "Next.jsで動画は再生されているのにモバイルだけエラーが出る問題に遭遇。原因はplay()メソッドとモバイルブラウザの自動再生制限でした。Safari / Chromeモバイルの仕様と実務での対処法を解説。"
summary: "Next.jsで動画は問題なく再生されているのに、モバイル端末だけエラーが表示される不可解な現象に遭遇。原因はplay()メソッドとモバイルブラウザの自動再生ポリシーでした。実体験をもとに原因と対処法を解説します。"
categories: ["Next.js", "フロントエンド", "トラブルシューティング"]
tags: ["Next.js", "React", "動画再生", "モバイル対応", "autoplay", "playメソッド", "DOMException", "ブラウザ仕様", "Web開発"]
showSummary: true
showHero: true
# heroImage: "featured.webp" # Page Bundle形式の場合は画像ファイルを置くだけでOK
---

{{< lead >}}
**「動画、ちゃんと再生されてるのに…なぜかエラーが出る」**  
しかも **モバイル端末だけ**。

PCでは問題なし、実機で動画も動いている。  
それなのに、コンソールには真っ赤なエラー。

今回は、Next.jsで動画再生を実装した際に実際に踏んだ  
**「モバイル特有の落とし穴」** と、その原因・対処法をまとめます。
{{< /lead >}}

---

## 起きた現象：動画は再生されるのにエラーが出る

実装していたのは、よくある動画再生処理です。

- Next.js（App Router）
- `<video>` 要素を useRef で取得
- マウント後に `video.play()` を呼ぶ

```tsx
useEffect(() => {
  videoRef.current?.play();
}, []);
````

### 状況整理

| 環境          | 結果                 |
| ----------- | ------------------ |
| PC Chrome   | 正常                 |
| PC Safari   | 正常                 |
| モバイル Safari | **動画は再生されるがエラー表示** |
| モバイル Chrome | **動画は再生されるがエラー表示** |

> 「え？再生されてるなら問題ないじゃん」

…そう思ったのは、**最初だけ**でした。

---

## 表示されていたエラー

モバイル端末のコンソールには、こんなエラーが出ていました。

```text
DOMException: play() failed because the user didn't interact with the document first.
```

もしくは：

```text
Uncaught (in promise) DOMException: The play() request was interrupted
```

### 厄介なポイント

* ❌ エラーが出ている
* ✅ でも動画は実際に再生されている
* ❌ エラーは Promise rejection 扱い
* ❌ Sentry などに大量に飛ぶ

**「動いてるけど、実装としては壊れている」**
一番やっかいな状態です。

---

## 原因：モバイルの自動再生ポリシーだった

結論から言うと、原因はこれでした。

> **モバイルブラウザの `play()` 自動再生制限**

### モバイルブラウザの基本ルール

Safari / Chrome（モバイル）では、以下が厳密に制限されています。

* ユーザー操作なしでの `video.play()`
* 音声付き動画の自動再生
* Promise を返す `play()` の失敗

つまり、

```ts
video.play()
```

は **「成功することもあるけど、エラーとして reject される」**
という **超わかりにくい挙動** をします。

---

## なぜ「再生されているのにエラー」になるのか

ここが一番ハマりポイントでした。

### 実際に起きていること

1. `video.play()` を実行
2. ブラウザが「自動再生制限」をチェック
3. **内部的には再生を許可**
4. しかし **Promise は reject**
5. コンソールにエラー表示

つまり、

> **再生結果と Promise の結果が一致していない**
>  
> つまり「UX上は成功」「API的には失敗」という、最悪に分かりづらい状態です。

という状態です。

これ、仕様です。

---

## ダメな実装例（私がやっていた）

```ts
videoRef.current?.play();
```

または

```ts
videoRef.current?.play().catch(console.error);
```

### 問題点

* モバイルでは `play()` が reject される
* 例外が発生し、エラー扱いになる
* ログ監視ツールが反応する

---

## 解決策①：play() の Promise を正しく扱う

最低限やるべき対処がこれです。

```ts
const video = videoRef.current;
if (!video) return;

const playPromise = video.play();

if (playPromise !== undefined) {
  playPromise.catch(() => {
    // モバイルの自動再生制限による reject は
  　// 再生可否とは無関係なため、エラー扱いしない
  });
}
```

### ポイント

* `play()` は Promise を返す前提で扱う
* モバイルの reject は「異常」ではない
* **ログに出さない設計が重要**

---

## 解決策②：ユーザー操作をトリガーにする（最も安全）

一番確実なのはこれです。

```tsx
<button onClick={() => videoRef.current?.play()}>
  再生する
</button>
```

### なぜ安全か

* ユーザー操作 = 自動再生制限を回避
* Safari / Chrome 両対応
* Promise が reject されにくい

> **「動画は必ずユーザー操作で再生させる」**
> これが最も事故らない設計です。

---

## 解決策③：muted + playsInline を正しく指定する

自動再生したい場合は、以下が必須です。

```tsx
<video
  ref={videoRef}
  muted
  playsInline
  autoPlay
/>
```

### 注意点

* `muted` がないとモバイルはほぼ失敗
* `playsInline` がないと全画面化される
* それでも `play()` の reject は起きうる

---

## 学び：Next.jsの問題ではなかった

最初は、完全に Next.js を疑っていました。

- Hydration のタイミング？
- useEffect の実行順？
- React Strict Mode？

でも結論はシンプルでした。

> **Next.jsは関係なく、完全にブラウザ仕様の問題**

---

## 実務での教訓

{{< alert icon="warning" >}}
**動画が「動いているか」ではなく
「エラーが出ていないか」を必ず確認する**
{{< /alert >}}

* モバイルの `play()` は信用しない
* Promise reject を前提に実装する
* Sentry / ログ監視と相性が悪い箇所は特に注意

---

## まとめ

* モバイルでは `play()` が **仕様上 reject される**
* 動画が再生されていてもエラーになる
* Promise を正しく扱う or ユーザー操作に寄せる
* Next.jsのバグではない

> **「動いてるのにエラーが出る」系は、だいたいブラウザ仕様**

同じ罠にハマった人の助けになれば嬉しいです。

## 📘 関連資料
{{< button href="https://developer.mozilla.org/ja/docs/Web/HTTP/Reference/Headers/Permissions-Policy/autoplay" >}}
Permissions-Policy: autoplay | MDN
{{< /button >}}
