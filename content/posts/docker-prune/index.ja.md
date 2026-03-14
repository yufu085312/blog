---

title: "Docker pruneとは？不要なイメージ・コンテナ・ボリュームを削除する方法"
date: 2026-03-14T17:37:00+09:00
draft: false
description: "Dockerのpruneコマンドについて解説。不要なコンテナ・イメージ・ネットワーク・ボリュームを削除する方法やdocker system pruneとの違いをわかりやすく紹介します。"
summary: "Dockerのpruneコマンドで不要なコンテナやイメージを削除する方法を解説。docker container prune、docker image prune、docker system pruneの違いも紹介します。"
slug: "docker-prune"
categories: ["インフラ"]
tags: ["Docker","コンテナ","DevOps"]
showSummary: true
showHero: true

# heroImage: "featured.webp"

---

{{< lead >}}
Dockerを使用していると、**不要なコンテナやイメージが溜まりディスク容量を圧迫する**ことがあります。

そのような場合に便利なのが **`docker prune` コマンド**です。

`docker prune` を使用すると、未使用のコンテナ・イメージ・ネットワークなどをまとめて削除できます。

この記事では **Dockerのpruneコマンドの使い方と注意点**を、実例付きでわかりやすく解説します。
{{< /lead >}}

---

## docker pruneとは？

`prune` は **不要なリソースを削除するためのDockerコマンド**です。

Dockerでは以下のようなデータが溜まりやすくなります。

* 停止したコンテナ
* 未使用のDockerイメージ
* 未使用のネットワーク
* 未使用のボリューム

`prune` を使用すると、これらの **未使用リソースを一括削除**できます。

---

## docker pruneで削除できるリソース

Dockerでは以下のリソースを削除できます。

| コマンド                　 | 内容 | 削除対象        |
| ------------------------ | ---- | ----------- |
| `docker container prune` | 停止コンテナ削除 |停止したコンテナ    |
| `docker image prune`     | 未使用イメージ削除 |未使用イメージ     |
| `docker volume prune`    | 未使用ボリューム削除 |未使用ボリューム    |
| `docker network prune`   | 未使用ネットワーク削除 |未使用ネットワーク   |
| `docker system prune`    | 全リソース削除 |すべての未使用リソース |

---

## docker container prune

停止しているコンテナを削除します。

```bash
docker container prune
```

実行すると以下の確認が表示されます。

```
WARNING! This will remove all stopped containers.
```

削除して問題ない場合は `y` を入力します。

---

## docker image prune

未使用のDockerイメージを削除します。

```bash
docker image prune
```

すべての未使用イメージを削除したい場合は `-a` を使用します。

```bash
docker image prune -a
```

---

## docker volume prune

未使用のボリュームを削除します。

```bash
docker volume prune
```

ボリュームはアプリケーションのデータが保存されている可能性があるため、
削除前に内容を確認することをおすすめします。

---

## docker network prune

未使用のネットワークを削除します。

```bash
docker network prune
```

---

## docker system prune

docker system prune は、
Dockerの未使用リソースをまとめて削除するコマンドです。

開発環境のクリーンアップで最もよく使われるコマンドです。

```bash
docker system prune
```

削除対象

* 停止コンテナ
* 未使用ネットワーク
* danglingイメージ
* ビルドキャッシュ

すべての未使用イメージも削除したい場合は `-a` を使用します。

```bash
docker system prune -a
```

### ボリュームも含めて削除する場合

```bash
docker system prune --volumes
```

---

## ディスク使用量を確認する

削除前にディスク使用量を確認したい場合は
以下のコマンドを使用します。

```bash
docker system df
```

例

```
TYPE            TOTAL     ACTIVE    SIZE
Images          10        4         3.2GB
Containers      6         1         120MB
Local Volumes   3         1         800MB
```

---

## Docker pruneの注意点

### 削除したデータは復元できない

`prune` で削除したリソースは **元に戻すことができません。**

重要なデータが含まれていないか確認してから実行してください。

---

### volume削除には注意

`docker volume prune` は **アプリケーションのデータを削除する可能性**があります。

特に以下のような環境では注意してください。

* データベース
* 永続データを保存しているアプリ

---

## よくあるエラー

### ボリュームが削除できない

以下のようなメッセージが表示されることがあります。

```
volume is in use
```

原因

ボリュームがコンテナで使用されているためです。

対処方法

使用しているコンテナを停止してから削除します。

```bash
docker stop container_name
```

---

## よく使うdocker pruneコマンド

開発環境のクリーンアップでは、以下のコマンドがよく使われます。

すべての未使用リソース削除

```bash
docker system prune
```

未使用イメージも削除

```bash
docker system prune -a
```

ボリュームも削除

```bash
docker system prune -a --volumes
```

---

## まとめ

Dockerでは、開発を続けていると不要なコンテナやイメージが溜まりやすくなります。

`docker prune` コマンドを使用することで

* 停止したコンテナ
* 未使用イメージ
* 未使用ボリューム
* 未使用ネットワーク

などを簡単に削除できます。

ディスク容量の節約や開発環境の整理のために、
定期的に `docker prune` を実行するのがおすすめです。

---

## 📘 関連資料

{{< button href="https://docs.docker.com/engine/manage-resources/pruning/" >}}Docker公式ドキュメント{{< /button >}}
