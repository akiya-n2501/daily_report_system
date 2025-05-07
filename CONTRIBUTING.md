# Contribution Guide

## ブランチ戦略

- GitHub Flow
  - main
  - feature

### ブランチ命名規則

- feature/[issue番号]_[タスク名]

- 例: feature/1_daily-report-model

## コミット

### コミット単位

キリの良いところで。

### メッセージ

機能名やクラス名等を含め、具体的に記載。

## Pull Request

### PR作成にあたって

- 該当するIssueへのリンク
- 詳細な説明
  - やったこと
    - 説明が必要なら、Files changedから追加
  - 単体テストの結果等の動作確認

- レビュアー
  - 結合テスト担当者
  - 栗原さん

- アサイニー
  - 自分

## コミュニケーション

### 目的

- コンフリクトを防ぐ

### 項目

- タスクの情報共有と対話
- Pull request受理後の連絡

### タスクの情報共有と対話

- タスクの情報共有
  - タスク
  - 時間帯
  - ブランチ名
  - 触るファイル
- 時間帯と触るファイルが被る人と対話し、調整をおこなう。

### Pull request受理後の連絡

- Pull request 受理後、mainブランチにマージ。
- mainブランチに更新が発生するため、それを他のメンバーに連絡。
- ほかのメンバーに対し、mainブランチを新しくすることを催促する。
  - `git pull origin main`
  - `git merge main`
