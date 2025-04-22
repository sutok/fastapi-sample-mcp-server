# ユーザー管理 API 仕様書

## 1. ユーザー情報取得

**概要**

- 説明：ログインユーザー自身の詳細情報を取得
- パス：`/api/v1/users/me`
- メソッド：`GET`
- 認証要件：必要

**リクエスト**

- 認証ヘッダーのみ必要

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "user_id": "string",
    "email": "string",
    "username": "string",
    "profile": {
      "display_name": "string",
      "phone_number": "string",
      "avatar_url": "string"
    },
    "created_at": "datetime",
    "updated_at": "datetime",
    "last_login_at": "datetime"
  }
}
```

## 2. ユーザー情報更新

**概要**

- 説明：ログインユーザーの情報を更新
- パス：`/api/v1/users/me`
- メソッド：`PATCH`
- 認証要件：必要

**リクエスト**

```json
{
  "username": {
    "型": "string",
    "必須": false,
    "バリデーション": "3-50文字",
    "説明": "ユーザー名"
  },
  "profile": {
    "型": "object",
    "必須": false,
    "説明": "プロフィール情報",
    "フィールド": {
      "display_name": {
        "型": "string",
        "必須": false,
        "バリデーション": "1-50文字"
      },
      "phone_number": {
        "型": "string",
        "必須": false,
        "バリデーション": "有効な電話番号形式"
      }
    }
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "user_id": "string",
    "email": "string",
    "username": "string",
    "profile": {
      "display_name": "string",
      "phone_number": "string",
      "avatar_url": "string"
    },
    "updated_at": "datetime"
  }
}
```

## 3. ユーザーアバター更新

**概要**

- 説明：ユーザーのプロフィール画像をアップロード
- パス：`/api/v1/users/me/avatar`
- メソッド：`PUT`
- 認証要件：必要

**リクエスト**

- Content-Type: `multipart/form-data`

```json
{
  "avatar": {
    "型": "file",
    "必須": true,
    "バリデーション": "最大5MB、許可形式: jpg, png, gif",
    "説明": "アバター画像ファイル"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "avatar_url": "string",
    "updated_at": "datetime"
  }
}
```

## 4. ユーザー一覧取得（管理者用）

**概要**

- 説明：システム内のユーザー一覧を取得
- パス：`/api/v1/users`
- メソッド：`GET`
- 認証要件：必要（管理者権限）

**リクエスト**

- クエリパラメータ

```json
{
  "page": {
    "型": "integer",
    "必須": false,
    "デフォルト値": 1,
    "説明": "ページ番号"
  },
  "per_page": {
    "型": "integer",
    "必須": false,
    "デフォルト値": 20,
    "バリデーション": "最大50",
    "説明": "1ページあたりの表示件数"
  },
  "search": {
    "型": "string",
    "必須": false,
    "説明": "検索キーワード（ユーザー名、メールアドレス）"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": [
    {
      "user_id": "string",
      "email": "string",
      "username": "string",
      "profile": {
        "display_name": "string",
        "avatar_url": "string"
      },
      "created_at": "datetime",
      "last_login_at": "datetime"
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 195,
    "per_page": 20
  }
}
```

## 5. 特定ユーザー情報取得（管理者用）

**概要**

- 説明：特定のユーザーの詳細情報を取得
- パス：`/api/v1/users/{user_id}`
- メソッド：`GET`
- 認証要件：必要（管理者権限）

**リクエスト**

- パスパラメータ

```json
{
  "user_id": {
    "型": "string",
    "必須": true,
    "説明": "対象ユーザーID"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "user_id": "string",
    "email": "string",
    "username": "string",
    "profile": {
      "display_name": "string",
      "phone_number": "string",
      "avatar_url": "string"
    },
    "created_at": "datetime",
    "updated_at": "datetime",
    "last_login_at": "datetime",
    "status": "active/suspended/deleted"
  }
}
```

## 6. ユーザーステータス更新（管理者用）

**概要**

- 説明：ユーザーのステータスを更新（アカウント停止など）
- パス：`/api/v1/users/{user_id}/status`
- メソッド：`PATCH`
- 認証要件：必要（管理者権限）

**リクエスト**

```json
{
  "status": {
    "型": "string",
    "必須": true,
    "許可値": ["active", "suspended"],
    "説明": "新しいステータス"
  },
  "reason": {
    "型": "string",
    "必須": false,
    "説明": "ステータス変更の理由"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "user_id": "string",
    "status": "string",
    "updated_at": "datetime"
  }
}
```

## 共通エラーレスポンス

### 権限エラー（403）

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "この操作を実行する権限がありません",
    "details": {
      "required_role": "admin"
    }
  }
}
```

### リソース未検出（404）

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "指定されたユーザーが見つかりません",
    "details": {
      "user_id": "要求されたID"
    }
  }
}
```

## セキュリティ仕様

1. アクセス制御

   - 一般ユーザーは自身の情報のみアクセス可能
   - 管理者ユーザーは全ユーザーの情報にアクセス可能

2. レート制限

   - 一般エンドポイント：60 回/分
   - 管理者用エンドポイント：120 回/分

3. データ保護
   - パスワードハッシュは返却しない
   - メールアドレスは管理者のみ表示
