---
title: 'Safariでwindow.openが動かない？非同期別タブ対処法'
date: 2026-01-21T23:01:39+09:00
draft: false
description: "Safariで非同期処理後にwindow.openが動かない原因と、別タブ遷移を安定させる2つの実践的な解決策を解説します。"
summary: "Safariで非同期処理後にwindow.openがブロックされ、別タブ遷移できない問題の原因と対処法を解説します。全ブラウザで安定動作する実務向けの実装パターンを紹介します。"
categories: ["JavaScript", "ブラウザ仕様"]
tags: ["Safari", "window.open", "async/await", "ポップアップブロック", "フロントエンド"]
showSummary: true
showHero: true
# heroImage: "featured.webp" # Page Bundle形式の場合は画像ファイルを置くだけでOK
---

{{< lead >}}
開発においてWebアプリで、非同期処理のあとに別タブを開こうとしたところ、Safariだけまったく反応しない、というトラブルに遭遇しました。

最初は実装ミスを疑いましたが、調べてみると原因はSafari特有の仕様でした。

本記事では、この実体験をもとに、なぜSafariだけ失敗するのか、そしてどう実装すれば安定するのかを整理して解説します。
{{< /lead >}}

## はじめに

Webアプリ開発でよくある要件のひとつに、

* ボタンをクリック
* APIを叩いてデータを作成
* 成功したら結果ページを**別タブで開く**

というフローがあります。

私自身、開発のでこの実装を行った際、**Chromeでは問題ないのにSafariだけ別タブが開かない** という現象に遭遇しました。

原因はコードのミスではなく、[Safari特有のポップアップ制御仕様](https://developer.mozilla.org/ja/docs/Web/API/Window/open)でした。

この記事では、

* なぜSafariだけ失敗するのか
* どう実装すれば全ブラウザで安定するのか

を、実務でそのまま使えるコード付きで解説します。
Webアプリで「ボタンをクリック → API呼び出し → 成功したら別タブで詳細ページを開く」といった実装はよくあります。しかし、**Safari だけ window.open が無視される / ポップアップブロックされる** という問題に遭遇したことはないでしょうか。

本記事では、Safari特有の仕様によって発生するこの問題の原因と、実務で使える具体的な対処法を解説します。

---

## 発生する問題の例

次のようなコードで、Chromeでは動くのにSafariでは新しいタブが開かないケースがあります。

```javascript
button.addEventListener('click', async () => {
  const res = await fetch('/api/create');
  const data = await res.json();

  // Safari ではここが無視される
  window.open(`/result/${data.id}`, '_blank');
});
```

* Chrome / Edge：正常に別タブで開く
* Safari：何も起きない（ポップアップブロック扱い）

---

## 原因：Safariの「ユーザー操作に紐づく同期実行」制限

Safariは、`window.open` を以下の条件でのみ許可します。

* **ユーザーの直接操作（clickなど）と“同期的に”実行されること**
* `await` や `setTimeout`、Promiseの then を跨ぐと「ユーザー操作由来ではない」と判定される

つまり、次のようなフローはSafariではNGです。

```
click
  ↓
await fetch()
  ↓
window.open()  ← もはやユーザー操作とみなされない
```

これはSafariのポップアップブロックポリシーによるものです。

---

## 対処法1：先に空のタブを開いてから遷移させる（最も実用的）

ユーザー操作の同期タイミングで、**先に空のタブを開いておく** 方法です。

```javascript
button.addEventListener('click', async () => {
  // ① ユーザー操作の同期中にタブを開く
  const newWindow = window.open('', '_blank');

  try {
    const res = await fetch('/api/create');
    const data = await res.json();

    // ② 後からURLを設定
    newWindow.location.href = `/result/${data.id}`;
  } catch (e) {
    // エラー時はタブを閉じる
    newWindow.close();
    alert('処理に失敗しました');
  }
});
```

### ポイント

* `window.open` は **必ず click ハンドラの同期部分で呼ぶ**
* 非同期処理後は `location.href` で遷移させる
* 失敗時は `close()` で空タブを閉じる

この方法は **Chrome / Safari / Firefox すべてで安定動作** します。

---

## 対処法2：非同期で取得したURLを事前に aタグに設定してから遷移させる

`window.open` を使わず、**事前に a タグの href を非同期で準備しておき、最終的な遷移は“純粋なユーザークリック”に任せる** 方法です。

Safariは「ユーザーが実際にクリックしたリンク遷移」については非常に寛容なため、この方法はポップアップブロックを回避できます。

### パターン1：pointerdown / mousedown で先にURLを準備する

```html
<a id="resultLink" target="_blank">結果を開く</a>
```

```javascript
const link = document.getElementById('resultLink');

// クリックより前のイベントで非同期処理を開始
link.addEventListener('pointerdown', async () => {
  if (link.dataset.ready) return;

  const res = await fetch('/api/create');
  const data = await res.json();

  // ここで事前にURLをセット
  link.href = `/result/${data.id}`;
  link.dataset.ready = 'true';
});
```

この実装では、

* `pointerdown`（または `mousedown`）で非同期処理を開始
* ユーザーがそのままクリックすると、**すでに設定済みの href に通常遷移**

となるため、Safariでもブロックされません。

### パターン2：2段階クリックで安全に遷移させる

UXを許容できる場合は、**1回目のクリックでURLを生成、2回目で遷移** という設計も有効です。

```html
<button id="prepare">リンクを生成</button>
<a id="resultLink" target="_blank" style="display:none;">結果を開く</a>
```

```javascript
document.getElementById('prepare').addEventListener('click', async () => {
  const res = await fetch('/api/create');
  const data = await res.json();

  const link = document.getElementById('resultLink');
  link.href = `/result/${data.id}`;
  link.style.display = 'inline';
});
```

この場合、最終的な遷移は完全にユーザー操作なので、**Safariの制限に引っかかりません**。

### この方法のメリット・デメリット

**メリット**

* `window.open` を使わないため、ポップアップブロックと無縁
* 実装がシンプルでブラウザ差異が少ない

**デメリット**

* UXを工夫しないと「クリックしてから少し待つ」挙動になる
* 1クリック完結型には向きにくい

---

## 対処法3：ユーザーに明示的にリンクをクリックさせる

Safariの制限を正面から回避する方法です。

```html
<a id="resultLink" target="_blank" style="display:none;">open</a>
```

```javascript
button.addEventListener('click', async () => {
  const res = await fetch('/api/create');
  const data = await res.json();

  const link = document.getElementById('resultLink');
  link.href = `/result/${data.id}`;
  link.click();
});
```

ただし、この方法でも環境によってはブロックされるため、**方法1の方が確実** です。

---

## 対処法3：遷移を同一タブにする（UX重視の場合）

業務アプリなどで別タブ必須でない場合は、単純に同一タブ遷移に変更するのも一つの手です。

```javascript
window.location.href = `/result/${data.id}`;
```

---

## よくあるNG例

### ❌ async/await の後に window.open

```javascript
await fetch(...);
window.open(url); // SafariではNG
```

### ❌ setTimeout 経由

```javascript
setTimeout(() => {
  window.open(url);
}, 0);
```

どちらも **ユーザー操作と切り離された実行** と判定され、Safariでブロックされます。

---

## 実務でのおすすめ実装パターン

最も安全で実績があるのは次の形です。

```javascript
button.addEventListener('click', async () => {
  const win = window.open('', '_blank');

  try {
    const res = await fetch('/api/create');
    const data = await res.json();

    win.location.replace(`/result/${data.id}`);
  } catch (e) {
    win.close();
    alert('エラーが発生しました');
  }
});
```

* `replace` を使えば履歴に空ページが残らない
* エラー時の UX も担保できる

---

## まとめ

Safariで `window.open` が非同期処理と組み合わさると失敗するのは、**ユーザー操作と同期していない処理を厳しくブロックする仕様**が原因です。

本記事の要点は次の3つです。

* Safariでは `await` の後の `window.open` は基本的に失敗する
* 解決策は **先に空タブを開く → 後からURLを設定する** パターン
* この方法は Chrome / Safari / Firefox すべてで安定動作する

非同期処理 × 別タブ遷移は、実務でも個人開発でもハマりやすいポイントです。

同じ問題で困っている方の助けになれば幸いです。`

---

## 📘 関連資料
{{< button href="https://developer.mozilla.org/ja/docs/Web/API/Window/open" >}}Window: open() メソッド - Web API - MDN Web Docs
{{< /button >}}
