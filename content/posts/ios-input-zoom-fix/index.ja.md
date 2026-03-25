---
title: "iOSでinputがズームされる原因と対策【ハーフモーダル対応】"
date: 2026-03-26T00:00:00+09:00
draft: false
description: "iOS Safariでハーフモーダル内のinputフォーカス時にズームされる問題の原因と解決方法を解説。font-size対策やviewport設定、Next.jsでの対応方法も紹介します。"
summary: "iOSでinputフォーカス時に画面が拡大される問題の原因と対策を解説。ハーフモーダルやBottom Sheetでの実装時の注意点も紹介します。"
slug: "ios-input-zoom-fix"
categories: ["フロントエンド"]
tags: ["iOS","Safari","Next.js","CSS","UI"]
showSummary: true
showHero: true
# heroImage: "featured.webp"
---

{{< lead >}}
iOS Safariでは、**inputにフォーカスしたときに画面が勝手にズームされる問題**があります。

特にハーフモーダル（Bottom Sheet）を実装している場合、

- 入力時に画面がズームしてレイアウトが崩れる
- モーダルが画面外にはみ出る
- 閉じるボタンが押せなくなる

といった問題が発生します。

この記事では、**iOSでinputが拡大される原因とその対策**を  
Next.jsでの実装例付きでわかりやすく解説します。

※ この挙動はiOS Safari特有の仕様であり、バグではありません。
{{< /lead >}}

---

## 結論

iOSでinputがズームされる原因は

👉 **font-sizeが16px未満**

です。

以下のCSSを設定すれば解決できます。

```css
input {
  font-size: 16px;
}
```

---

## 対象環境

- iOS Safari
- iPhone / iPad
- Next.js / React

---

## 問題の概要

iOS Safariでは、inputにフォーカスすると自動でズームされることがあります。

特に以下のようなケースで発生します。

- ハーフモーダル内のinput
- 小さいフォントサイズ
- スマホUI

---

## なぜズームされるのか

原因は **フォントサイズが16px未満**であることです。

iOS Safariは、可読性を確保するために

👉 小さい文字のinputにフォーカスすると自動ズーム

という仕様になっています。

---

### 補足：line-heightにも注意

極端に小さいline-heightを指定している場合、
意図しないズーム挙動になることがあります。

---

## 解決方法①：font-sizeを16px以上にする（最重要）

これが最もシンプルで確実な解決方法です。

```css
input,
textarea,
select {
  font-size: 16px;
}
````

👉 これだけでズームは防げます

---

## Tailwind CSSでの対応

```tsx
<input className="text-base" />
```

※ `text-base` = 16px

---

## 解決方法②：viewportでズームを無効化（非推奨）

以下のように設定するとズームを防ぐことができます。

```html
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
```

しかし、この方法は問題があります。

---

### ⚠️ デメリット

* ユーザーのピンチズームができなくなる
* アクセシビリティ低下
* Appleのガイドライン的にも非推奨

👉 基本は **使わない方が良いです**

---

## 解決方法③：transformスケールで調整（応用）

デザイン上どうしても小さく見せたい場合

```css
input {
  font-size: 16px;
  transform: scale(0.9);
}
```

👉 見た目だけ小さくできます

---

## ハーフモーダルで発生する問題

Bottom Sheetでは以下の問題が発生しやすいです。

* フォーカス時に画面がズレる
* モーダルが上に押し上がる
* スクロール位置が崩れる

---

## 対策：viewport高さ問題も同時に対応する

iOSではキーボード表示時に高さが変わります。

```css
height: 100vh;
```

は使わず👇

```css
height: 100dvh;
```

を使用します。

---

## Next.jsでの実装例

```tsx
"use client";

export default function BottomSheet() {
  return (
    <div className="fixed inset-0 bg-black/50">
      <div className="fixed bottom-0 w-full bg-white p-4 rounded-t-2xl">
        <input
          className="w-full border p-2 text-base"
          placeholder="メールアドレス"
        />
      </div>
    </div>
  );
}
```

---

## よくある間違い

### font-sizeを14pxにしている

```css
input {
  font-size: 14px; // NG
}
```

👉 これがズームの原因です

---

### Tailwindで小さい文字を使っている

```tsx
<input className="text-sm" /> // NG
```

---

## よくあるハマりポイント

- デザイン優先でtext-smを使ってしまう
- PCでは問題なく気づかない
- iOS実機で初めて気づく

---

## FAQ

### なぜAndroidでは起きないの？

Android Chromeにはこの仕様がないためです。

---

### inputだけでなくtextareaも対象？

はい、同様にズームされます。

---

### デザイン的に16pxは大きすぎる場合は？

👉 transformで縮小するのがおすすめです

---

## 実務でのおすすめ設定

```css
input,
textarea,
select {
  font-size: 16px;
}
```

* Tailwindなら `text-base`
* 小さく見せたい場合は `transform: scale`

---

## まとめ

iOSでinputフォーカス時にズームされる原因は

👉 **font-sizeが16px未満**

です。

対策はシンプルで

* font-sizeを16px以上にする（推奨）
* viewport制御（非推奨）
* transformで見た目調整

ハーフモーダルでは特に影響が大きいため、
最初からこの仕様を考慮して設計することが重要です。
