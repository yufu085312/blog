---

title: 'TypeScriptの型アサーションとは？使い方と注意点をわかりやすく解説'
date: 2026-03-10T01:00:00+09:00
draft: false
description: "TypeScriptの型アサーション（Type Assertion）の使い方を解説します。as構文や<>構文の違い、as constやNon-null assertion、よくあるエラーまで初心者向けに紹介します。"
summary: "TypeScriptの型アサーションとは何かを初心者向けに解説。as構文の使い方やas const、Non-null assertion、よくあるエラーについて紹介します。"
slug: "typescript-type-assertion"
categories: ["フロントエンド"]
tags: ["TypeScript","JavaScript","型","プログラミング"]
showSummary: true
showHero: true

# heroImage: "featured.webp"

---

{{< lead >}}
TypeScriptでは、変数の型を明示的に指定することで安全なコードを書くことができます。
しかし、実際の開発では「この値はこの型であると開発者が確信している」ケースもあります。

そのような場合に使用するのが**型アサーション**（Type Assertion）です。

この記事では、TypeScriptの型アサーションについて、基本的な使い方から注意点、`as const`やNon-null assertionまでわかりやすく解説します。
{{< /lead >}}

---

## 型アサーションとは

型アサーションとは、**開発者が値の型を明示的に指定する仕組み**です。

TypeScriptの型推論では正しい型が判断できない場合に、
「この値はこの型として扱ってほしい」とコンパイラに伝えることができます。

簡単に言うと、

> **「この値はこの型だと開発者が保証する」**

という仕組みです。

---

## 型アサーションの基本構文

型アサーションには主に2つの書き方があります。

### as構文

```ts
const value = "hello" as string
```

現在のTypeScriptでは、**as構文が推奨されています。**

---

### <>構文

```ts
const value = <string>"hello"
```

ただし、JSX（Reactなど）では構文が衝突するため、
通常は **as構文を使用することが一般的**です。

---

## 型アサーションの使用例

### DOM要素の取得

DOM操作では型アサーションがよく使用されます。

```ts
const input = document.getElementById("name") as HTMLInputElement

console.log(input.value)
```

`getElementById` の戻り値は

```ts
HTMLElement | null
```

のため、そのままでは `value` にアクセスできません。

型アサーションを使うことで `HTMLInputElement` として扱えます。

---

### unknown型の変換

```ts
const value: unknown = "Hello"

const str = value as string

console.log(str.length)
```

---

## 型アサーションの注意点

型アサーションは便利ですが、**使いすぎには注意が必要です。**

理由は、TypeScriptの型チェックを**強制的に回避してしまう**ためです。

例

```ts
const num = "hello" as unknown as number
```

これは実行時に問題が起きる可能性があります。

---

## 型アサーションと型変換の違い

型アサーションは**実際の型変換ではありません。**

例

```ts
const value = "123" as number
```

これはJavaScriptの値としては**文字列のまま**です。

実際に数値へ変換する場合は以下を使用します。

```ts
Number("123")
```

---

## 型アサーションを使うべきケース

型アサーションが有効なケース

* DOM操作
* APIレスポンスの型指定
* unknown型の変換
* ライブラリの型が不完全な場合

---

## as constとは

`as const` は、値を**リテラル型として固定するための型アサーション**です。

例

```ts
const user = {
  name: "John",
  age: 20
} as const
```

この場合、型は以下のようになります。

```ts
{
  readonly name: "John"
  readonly age: 20
}
```

特徴

* 値が変更不可（readonly）
* リテラル型になる

通常のオブジェクト

```ts
const user = {
  name: "John"
}
```

型

```ts
{
  name: string
}
```

`as const` を使うと **より厳密な型**になります。

---

## Non-null assertionとは

TypeScriptには **Non-null assertion（ノンヌルアサーション）** という書き方があります。

これは **値がnullまたはundefinedではないと保証する記法**です。

構文

```ts
value!
```

例

```ts
const element = document.getElementById("app")!

console.log(element.innerHTML)
```

通常 `getElementById` の型は

```ts
HTMLElement | null
```

ですが、`!` を使うことで **nullではないとTypeScriptに伝えます。**

---

## TypeScriptでよくあるエラー

型アサーションを使う場面でよくあるエラーを紹介します。

### Type 'unknown' is not assignable to type

例

```ts
const value: unknown = "hello"

const str: string = value
```

エラーになります。

解決方法

```ts
const str = value as string
```

---

### Object is possibly 'null'

例

```ts
const element = document.getElementById("app")

console.log(element.innerHTML)
```

この場合 `element` が `null` の可能性があるためエラーになります。

解決方法

```ts
const element = document.getElementById("app")!
```

または

```ts
if (element) {
  console.log(element.innerHTML)
}
```

---

## まとめ

TypeScriptの型アサーションは、開発者が値の型を明示的に指定する仕組みです。

ポイント

* `as` 構文を使うのが一般的
* 型推論が難しい場合に便利
* `as const` でリテラル型にできる
* `!` でNon-null assertionができる
* 使いすぎると型安全性が下がる

適切に利用することで、TypeScriptの型システムをより柔軟に活用できます。

---

## 📘 関連資料

<div class="flex flex-col gap-2 items-start">

{{< button href="https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions" >}}TypeScript公式ドキュメント{{< /button >}}

{{< button href="https://www.typescriptlang.org/docs/" >}}TypeScriptドキュメント{{< /button >}}

</div>
