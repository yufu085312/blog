---
title: "Next.jsでハーフモーダル（Bottom Sheet）を実装する方法"
date: 2026-03-20T02:30:00+09:00
draft: false
description: "Next.jsでハーフモーダル（Bottom Sheet）を実装する方法を解説。CSSのみの実装からReactでの状態管理、アニメーション付きUIまで紹介します。"
summary: "Next.jsでハーフモーダル（Bottom Sheet）を実装する方法を紹介。useStateによる制御やアニメーション、スマホUIの最適化まで解説します。"
slug: "nextjs-half-modal"
categories: ["フロントエンド"]
tags: ["Next.js","React","UI","CSS"]
showSummary: true
showHero: true

# heroImage: "featured.webp"
---

{{< lead >}}
スマートフォン向けUIでよく使われるのが、画面下からスライドして表示される **ハーフモーダル（Bottom Sheet）** です。

アプリの詳細表示やアクションメニューなどでよく利用され、UX向上に役立ちます。

この記事では **Next.jsでハーフモーダルを実装する方法**を、基本から応用までわかりやすく解説します。

※ 本記事のコードは **Next.js App Router** を前提としています。
{{< /lead >}}

---

## ハーフモーダル（Bottom Sheet）とは

ハーフモーダルとは、**画面の下部から表示されるモーダルUI**のことです。

特徴

* 画面を覆いすぎない
* スマホ操作と相性が良い
* UXを向上させる

---

## 実装の基本構成

ハーフモーダルは以下の要素で構成されます。

* オーバーレイ（背景）
* モーダル本体
* 開閉状態の管理

---

## useStateでハーフモーダルを制御する

まずは基本的な実装です。

```tsx
"use client";

import { useState } from "react";

export default function Page() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(true)}>
        モーダルを開く
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black/50">
          <div className="fixed bottom-0 w-full bg-white p-4 rounded-t-2xl">
            <button onClick={() => setIsOpen(false)}>
              閉じる
            </button>
            <p>ハーフモーダルです</p>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## Next.jsでの注意点（SSR）
Next.jsではServer ComponentとClient Componentの違いに注意が必要です。

今回のようなモーダル操作はブラウザAPIを使用するため、
必ず **"use client"** を付ける必要があります。

```tsx
"use client";
```
これが無いとエラーになるため注意してください。

---

## アニメーションを追加する

UXを向上させるためにアニメーションを追加します。

```css
.modal {
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.modal.open {
  transform: translateY(0);
}
```

---

## Tailwind CSSで実装する例

```tsx
<div
  className={`fixed bottom-0 w-full bg-white p-4 rounded-t-2xl transition-transform duration-300 ${
    isOpen ? "translate-y-0" : "translate-y-full"
  }`}
>
```

---

## 外側クリックで閉じる

UX改善として重要です。

```tsx
<div
  className="fixed inset-0 bg-black/50"
  onClick={() => setIsOpen(false)}
>
  <div onClick={(e) => e.stopPropagation()}>
    モーダル内容
  </div>
</div>
```

---

## アクセシビリティ対応（a11y）

モーダルUIではアクセシビリティ対応も重要です。

### フォーカス制御

モーダル表示時はフォーカスを内部に移動します。

```tsx
useEffect(() => {
  if (isOpen) {
    document.getElementById("modal")?.focus();
  }
}, [isOpen]);
````

---

### aria属性

```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
```

---

### ESCキーで閉じる

```tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") setIsOpen(false);
  };

  window.addEventListener("keydown", handleKeyDown);
  return () => window.removeEventListener("keydown", handleKeyDown);
}, []);
```

👉 アクセシビリティ対応をすることで、**実務レベルのUI実装になります。**

---

## ハーフモーダル実装におすすめのライブラリ比較

ハーフモーダルは自作も可能ですが、UIライブラリを利用すると効率的に実装できます。

ここでは代表的なライブラリを比較します。

---

### react-modal

シンプルなモーダルライブラリです。

特徴

* 軽量で導入が簡単
* 基本的なモーダル機能のみ提供
* カスタマイズ前提

向いているケース

* 最小構成で実装したい
* デザインを自作したい

---

### Radix UI

アクセシビリティに優れたUIライブラリです。

特徴

* 高品質なUIコンポーネント
* キーボード操作・アクセシビリティ対応
* 柔軟なカスタマイズ

向いているケース

* 本格的なプロダクト開発
* UI品質を重視する場合

---

### Headless UI

Tailwind CSSと相性の良いUIライブラリです。

特徴

* 見た目を持たない（ロジックのみ）
* Tailwindで自由にデザイン可能
* Reactとの親和性が高い

向いているケース

* Tailwind CSSを使用している
* デザインを完全にカスタムしたい

---

### まとめ（ライブラリ選定）

| ライブラリ       | 特徴   | おすすめ用途     |
| ----------- | ---- | ---------- |
| react-modal | シンプル | 小規模・検証     |
| Radix UI    | 高機能  | 本番プロダクト    |
| Headless UI | 柔軟   | Tailwind環境 |

👉 **スマホUI（Bottom Sheet）を本格的に作る場合は、Radix UI or Headless UIがおすすめです。**

---

## スワイプで閉じるハーフモーダルの実装

スマホUIでは、**スワイプ操作でモーダルを閉じる**ことでUXが大幅に向上します。

---

### 実装の考え方

スワイプ対応は以下の流れで実装します。

1. タッチ開始位置を取得
2. 移動距離を計算
3. 一定距離で閉じる

---

### 実装例

```tsx
"use client";

import { useState, useRef } from "react";

export default function BottomSheet() {
  const [isOpen, setIsOpen] = useState(true);
  const startY = useRef(0);

  const handleTouchStart = (e: React.TouchEvent) => {
    startY.current = e.touches[0].clientY;
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    const currentY = e.touches[0].clientY;
    const diff = currentY - startY.current;

    // 下方向にスワイプした場合のみ
    if (diff > 100) {
      setIsOpen(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50">
      <div
        className="fixed bottom-0 w-full bg-white p-4 rounded-t-2xl"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
      >
        <div className="w-12 h-1 bg-gray-300 mx-auto mb-2 rounded" />
        <p>スワイプで閉じるモーダル</p>
      </div>
    </div>
  );
}
```

---

### ドラッグに追従する実装

```tsx
const [translateY, setTranslateY] = useState(0);

const handleTouchMove = (e: React.TouchEvent) => {
  const currentY = e.touches[0].clientY;
  const diff = currentY - startY.current;

  if (diff > 0) {
    setTranslateY(diff);
  }
};

const handleTouchEnd = () => {
  if (translateY > 100) {
    setIsOpen(false);
  } else {
    setTranslateY(0);
  }
};

<div
  style={{ transform: `translateY(${translateY}px)` }}
>
```

👉 これで **ネイティブアプリっぽくなる**
👉 SEO的にも「実装深い記事」扱いになる

---

### スクロールとの競合対策

モーダル内部がスクロール可能な場合、
スワイプとスクロールが競合することがあります。

対策

* モーダル上部のみドラッグ可能にする
* 一定位置でのみスワイプ検知する

---

### UXを良くするポイント

* ドラッグ中に位置を追従させる（transformで移動）
* スワイプ速度も考慮する
* 上方向スワイプは無効化

---

### 注意点

* PCではスワイプは動作しない（タッチ限定）
* iOS Safariで挙動差が出る場合あり
* スクロールとの競合に注意

---

## ハーフモーダルの注意点

### スクロール制御

モーダル表示中は背景スクロールを止めるのが一般的です。

```tsx
import { useState, useEffect } from "react";

useEffect(() => {
  document.body.style.overflow = isOpen ? "hidden" : "auto";
}, [isOpen]);
```

---

### z-index管理

他のUIと重なる場合は z-index を調整します。

---

## よくあるエラー

### モーダルが背面に表示される

原因

z-indexが低い

対処

```css
z-index: 50;
```

---

### スクロールが効いてしまう

背景スクロールを制御していない可能性があります。

---

## よくある質問

### ハーフモーダルと通常のモーダルの違いは何ですか？

ハーフモーダル（Bottom Sheet）は、画面全体を覆わずに**下部から表示されるモーダルUI**です。
一方、通常のモーダルは画面全体を覆うため、ユーザーの操作を完全に遮断します。

ハーフモーダルは特にスマートフォンでの操作性が高く、UX向上に適しています。

---

### ハーフモーダルはライブラリを使うべきですか？

用途によって異なります。

* シンプルなUI → 自作で十分
* 本格的なプロダクト → ライブラリ推奨

特にアクセシビリティやアニメーションを考慮する場合は、
Radix UIやHeadless UIなどの利用がおすすめです。

---

### スワイプ対応は必須ですか？

必須ではありませんが、スマホUIでは**実装することを強くおすすめ**します。

スワイプで閉じられることで、ネイティブアプリに近い操作感になり、UXが大きく向上します。

---

### PCでもハーフモーダルは使えますか？

使用可能ですが、PCでは一般的に**通常のモーダルの方が適しています**。

ハーフモーダルはタッチ操作を前提としたUIのため、
スマートフォンやタブレットで特に効果を発揮します。

---

### スクロールとスワイプが競合する場合はどうすればいいですか？

以下の対策が有効です。

* モーダル上部のみドラッグ可能にする
* スクロールが最上部のときのみスワイプを有効にする
* `touch-action` を調整する

これにより、意図しない挙動を防ぐことができます。

---

### アクセシビリティ対応は必要ですか？

はい、重要です。

モーダルUIでは以下の対応が推奨されます。

* `role="dialog"` の付与
* フォーカス制御
* ESCキーで閉じる

これらを実装することで、より多くのユーザーにとって使いやすいUIになります。

---

### Next.jsで実装する際の注意点はありますか？

ハーフモーダルは `useState` や `useEffect` を使用するため、
**Client Componentとして実装する必要があります。**

```tsx
"use client";
```

これを付けないと、イベントや状態管理が正しく動作しないため注意してください。

---

## まとめ

Next.jsでは、Reactの状態管理を使うことで
ハーフモーダル（Bottom Sheet）を簡単に実装できます。

主なポイント

* useStateで開閉管理
* CSSでアニメーション
* 外側クリックで閉じる
* スクロール制御

スマホUIの改善に非常に有効なので、ぜひ活用してみてください。

---

## 📘 関連資料

{{< button href="https://react.dev/" >}}React公式ドキュメント{{< /button >}}
