---
title: "Next.jsでiOS・Android・WebをUser-Agentで判定する方法【デバイス判定】"
date: 2026-03-14T00:00:00+09:00
draft: false
description: "Next.jsでユーザーエージェント（User-Agent）を利用してiOS、Android、Webを判定する方法を解説。middlewareやserver componentでの実装例も紹介します。"
summary: "Next.jsでUser-Agentを使ってiOS・Android・Webを判定する方法を紹介。server componentやmiddlewareでの実装例も解説します。"
slug: "nextjs-user-agent-detect"
categories: ["フロントエンド"]
tags: ["Next.js","User-Agent","JavaScript","React"]
showSummary: true
showHero: true
# heroImage: "featured.webp"
---

{{< lead >}}
Webアプリでは、**ユーザーのデバイスに応じて処理を分岐したい場面**があります。

例えば以下のようなケースです。

- iOSユーザーのみアプリストアへ誘導
- AndroidユーザーはGoogle Playへ誘導
- PCユーザーにはWeb版を表示

このような場合、**User-Agent**（ユーザーエージェント）を利用することで  
iOS・Android・Webを判定できます。

この記事では **Next.jsでUser-Agentを利用してデバイス判定を行う方法**を  
実装例付きでわかりやすく解説します。

※ 本記事のコードは **Next.js App Router** を前提としています。
{{< /lead >}}

---

## User-Agentとは

**User-Agent**（ユーザーエージェント）とは、  
ブラウザやOSなどの情報をサーバーに伝えるHTTPヘッダーです。

例

```
Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)

```

この文字列から以下のような情報を取得できます。

- OS（iOS / Android / Windows / macOS）
- ブラウザ（Chrome / Safari / Edge）
- デバイス（スマートフォン / PC）

---

## Next.jsでUser-Agentを取得する方法

Next.jsでは以下の方法でUser-Agentを取得できます。

- Server Component
- Middleware
- API Route

今回は **Server Componentでの判定方法**を紹介します。

---

### Server ComponentでUser-Agentを取得する

Next.jsでは `headers()` を使用することで  
リクエストヘッダーを取得できます。

```tsx
import { headers } from "next/headers";

export default function Page() {
  const userAgent = headers().get("user-agent") || "";

  return <div>{userAgent}</div>;
}
```

これで **User-Agent文字列を取得**できます。

---

## iOS / Android / Webを判定する

User-Agentを文字列判定することで
OSを判定できます。

```tsx
import { headers } from "next/headers";

export default function Page() {

  const ua = headers().get("user-agent") || "";

  const isIOS = /iPhone|iPad|iPod/.test(ua);
  const isAndroid = /Android/.test(ua);

  let device = "Web";

  if (isIOS) device = "iOS";
  if (isAndroid) device = "Android";

  return (
    <div>
      device: {device}
    </div>
  );
}
```

判定結果

| デバイス       | 判定      |
| ---------- | ------- |
| iPhone     | iOS     |
| Androidスマホ | Android |
| PCブラウザ     | Web     |

---

## ユーティリティ関数として作る

実務では **関数化するのがおすすめ**です。

```ts
export function getDeviceType(userAgent: string) {

  const isIOS = /iPhone|iPad|iPod/.test(userAgent);
  const isAndroid = /Android/.test(userAgent);

  if (isIOS) return "ios";
  if (isAndroid) return "android";

  return "web";
}
```

使用例

```tsx
import { headers } from "next/headers";
import { getDeviceType } from "@/lib/device";

export default function Page() {

  const ua = headers().get("user-agent") || "";
  const device = getDeviceType(ua);

  return <div>{device}</div>;
}
```

---

## MiddlewareでUser-Agentを判定する

Next.jsでは **Middleware** を利用して、リクエストの段階で  
User-Agentを判定することもできます。

Middlewareを使用すると、ページが表示される前に  
デバイスごとの処理を実行できます。

例えば、以下のような用途があります。

- iOSユーザーをApp Storeへリダイレクト
- AndroidユーザーをGoogle Playへリダイレクト
- PCユーザーは通常のWebページを表示

### 実装例

以下はMiddlewareでUser-Agentを取得する例です。

```ts
import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {

  const ua = request.headers.get("user-agent") || "";

  const isIOS = /iPhone|iPad|iPod/.test(ua);
  const isAndroid = /Android/.test(ua);

  if (isIOS) {
    return NextResponse.redirect("https://apps.apple.com");
  }

  if (isAndroid) {
    return NextResponse.redirect("https://play.google.com");
  }

  return NextResponse.next();
}
````

このように **User-Agentを判定してリダイレクト処理**を行うことができます。

### Middlewareの設置場所

Middlewareは以下のファイルとして作成します。

```
/middleware.ts
```

Next.jsではこのファイルが自動的に認識され、
すべてのリクエストに対してMiddlewareが実行されます。

特定のページのみ適用したい場合は、`matcher` を設定することも可能です。

```ts
export const config = {
  matcher: ["/app/:path*"],
};
```

これにより `/app` 以下のページのみにMiddlewareを適用できます。

---

## App Store / Google Playへリダイレクトする例

デバイスに応じてストアへ誘導することもできます。

```ts
import { redirect } from "next/navigation";

if (device === "ios") {
  redirect("https://apps.apple.com/app/xxxx");
}

if (device === "android") {
  redirect("https://play.google.com/store/apps/details?id=xxxx");
}
```

---

## User-Agent判定の注意点

User-Agent判定にはいくつか注意点があります。

### User-Agentは偽装できる

User-Agentはブラウザ側で変更可能なため、
**完全なデバイス判定ではありません。**

---

### 将来変更される可能性がある

ブラウザの仕様変更により
User-Agentのフォーマットが変わる可能性があります。

---

### ライブラリを使用する方法もある

より正確に判定する場合は
以下のライブラリを使用する方法もあります。

* ua-parser-js
* device-detector-js

---

## よくあるエラー

Next.jsでUser-Agentを取得する際に、  
以下のエラーが発生することがあります。

### headers() が使えない

以下のようなエラーが表示される場合があります。

```
Error: headers() can only be used in a Server Component

```

原因

`headers()` は **Server Component専用API** のため、  
Client Componentでは使用できません。

対処方法

- Server Componentで使用する
- MiddlewareでUser-Agentを取得する

---

### User-Agentが取得できない

以下のように `null` が返る場合があります。

```ts
const ua = headers().get("user-agent")
```

この場合は **nullチェック** を行うようにします。

```ts
const ua = headers().get("user-agent") || ""
```

これにより安全にUser-Agentを扱うことができます。

---

## まとめ

Next.jsでは `headers()` を利用することで  
User-Agentを取得できます。

これにより

・iOS  
・Android  
・Web  

などのデバイス判定が可能になります。

また、Middlewareを利用することで  
ユーザーのデバイスに応じてリダイレクト処理も実装できます。

User-Agentは偽装可能な情報のため、  
完全なデバイス判定ではなく **補助的な判定として利用することが推奨されています。**
