---
title: "CSSにおけるプリミティブカラーとセマンティックカラーの違いと設計方法"
date: 2026-03-31T00:00:00+09:00
draft: false
description: "CSS設計におけるプリミティブカラーとセマンティックカラーの違いを解説。状態別カラーやコンポーネント設計、Figma連携まで実務レベルで紹介します。"
summary: "プリミティブカラーとセマンティックカラーの違いと使い分けを解説。hover・disabled対応やコンポーネント設計、Figma連携まで実例付きで紹介します。"
slug: "css-color-design"
categories: ["フロントエンド"]
tags: ["CSS","デザインシステム","UI","Tailwind"]
showSummary: true
showHero: true
---

{{< lead >}}
CSS設計において、**カラー設計は非常に重要な要素**です。

特に近年では、デザインシステムの普及により

- プリミティブカラー（Primitive Color）
- セマンティックカラー（Semantic Color）

という概念が重要になっています。

この記事では、**2つの違いと実務で使える設計方法**を  
実装例付きでわかりやすく解説します。
{{< /lead >}}

---

## プリミティブカラーとは

プリミティブカラーとは、**純粋な色そのものを定義したもの**です。

```css
:root {
  --blue-500: #3b82f6;
  --red-500: #ef4444;
  --gray-100: #f3f4f6;
}
````

特徴

* 色そのものを表す
* UIの意味は持たない
* デザインのベース

👉 **カラーパレット**

---

## セマンティックカラーとは

セマンティックカラーとは、**役割（意味）を持った色**です。

```css
:root {
  --color-primary: var(--blue-500);
  --color-danger: var(--red-500);
  --color-background: var(--gray-100);
}
```

特徴

* UIの意味を表す
* デザイン変更に強い
* 再利用しやすい

👉 **役割ベースのカラー**

---

## カラー設計のレイヤー構造

実務では、カラーは以下の3階層で管理します。

1. プリミティブカラー（色そのもの）
2. セマンティックカラー（意味）
3. コンポーネントカラー（UI単位）

例：

```css
primitive → semantic → component
```

```css
--blue-500
　　↓
--color-primary
　　↓
--button-bg
```

---

## 違いまとめ

| 種類      | 内容     | 例                |
| ------- | ------ | ---------------- |
| プリミティブ  | 色そのもの  | blue-500         |
| セマンティック | 意味を持つ色 | primary / danger |

---

## なぜセマンティックカラーが重要なのか

### デザイン変更に強い

```css
--color-primary: var(--blue-500);
```

↓

```css
--color-primary: var(--green-500);
```

👉 UI修正なしで色変更できる

---

### 可読性が上がる

```css
color: var(--color-danger);
```

👉 意味が明確

---

### チーム開発に強い

* デザイナーと共通言語
* 一貫性を維持

---

## セマンティックカラーの粒度

セマンティックカラーは用途ごとに分けるのが重要です。

- primary（メインカラー）
- secondary（補助）
- success（成功）
- warning（警告）
- danger（エラー）
- info（情報）

👉 状態や意味ごとに分けることで拡張しやすくなります

---

## 状態別カラー（hover / disabled）

実務では「状態」によって色を変える必要があります。

### 設計例

```css
:root {
  --color-primary: var(--blue-500);
  --color-primary-hover: var(--blue-600);
  --color-primary-disabled: var(--gray-400);
}
```

使用例

```css
.button {
  background: var(--color-primary);
}

.button:hover {
  background: var(--color-primary-hover);
}

.button:disabled {
  background: var(--color-primary-disabled);
}
```

👉 状態もセマンティックとして管理するのがポイント

---

## 命名ルールのベストプラクティス

良い例：

```css
--color-primary
--color-primary-hover
--button-bg
```

悪い例：

```css
--main-color
--blue
```

---

## コンポーネント単位の設計

さらに発展させると、**コンポーネント単位で色を定義**します。

```css
:root {
  --button-bg: var(--color-primary);
  --button-text: #fff;
  --button-hover: var(--color-primary-hover);
}
```

```css
.button {
  background: var(--button-bg);
  color: var(--button-text);
}
```

メリット

* UI変更に強い
* コンポーネントごとに最適化できる

👉 **デザインシステムに近づく**

---

## Tailwind CSSでの設計

### プリミティブ

```js
colors: {
  blue: {
    500: "#3b82f6",
  }
}
```

---

### セマンティック

```js
colors: {
  primary: "var(--color-primary)",
}
```

👉 CSS変数と組み合わせるのがベスト

---

## 導入手順（実務フロー）

1. プリミティブカラーを定義
2. セマンティックカラーを作成
3. コンポーネントに割り当てる
4. Tailwind or CSSで利用

👉 いきなりセマンティックから作らないのがポイント

---

## Tailwindでの実務パターン

Tailwindでは、CSS変数をベースに設計するのがおすすめです。

```js
// tailwind.config.js
theme: {
  colors: {
    primary: "var(--color-primary)",
  }
}
```

👉 Tailwind × CSS変数で
「デザイン変更に強い構成」を作れる

---

## ダークモード対応

```css
:root {
  --color-background: #ffffff;
}

[data-theme="dark"] {
  --color-primary: var(--blue-400);
}
```

👉 セマンティックなら簡単に切り替え可能

---

## Figmaとの連携

デザインツールとの連携も重要です。

### Figma側

* primitive（color palette）
* semantic（role color）

を分けて定義

例

* Blue / 500（primitive）
* Primary / Default（semantic）

---

### 開発側

```css
--blue-500: #3b82f6;
--color-primary: var(--blue-500);
```

👉 デザインとコードを一致させる

---

## NGパターン

### 直接色を書く

```css
color: #3b82f6;
```

👉 修正が大変

---

### 意味のない名前

```css
--color-main
```

👉 NG（曖昧）

---

### プリミティブを直接使う

```css
color: var(--blue-500);
```

👉 意味が伝わらない

---

### セマンティックを飛ばしてしまう

--blue-500 を直接使う

👉 NG理由：
デザイン変更時に全修正が必要になる

---

## 実務での設計例

```css
:root {
  /* primitive */
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --gray-100: #f3f4f6;
  --gray-400: #9ca3af;

  /* semantic */
  --color-primary: var(--blue-500);
  --color-primary-hover: var(--blue-600);
  --color-primary-disabled: var(--gray-400);
  --color-bg: var(--gray-100);

  /* component */
  --button-bg: var(--color-primary);
}
```

---

## まとめ

CSSのカラー設計では

* プリミティブカラー（色）
* セマンティックカラー（役割）

を分けることが重要です。

さらに

* 状態別カラー
* コンポーネント設計
* Figma連携

まで行うことで、**実務で通用する設計**になります。

---

👉 **結論：セマンティックカラー中心で設計するのがベスト**
