# 認証関連 API 仕様書

## 1. サインアップ

**概要**

- 説明：新規ユーザーの登録
- パス：`/api/v1/auth/signup`
- メソッド：`POST`
- 認証要件：不要

**リクエスト**

```json
{
  "email": {
    "型": "string",
    "必須": true,
    "バリデーション": "有効なメールアドレス形式",
    "説明": "ユーザーのメールアドレス"
  },
  "password": {
    "型": "string",
    "必須": true,
    "バリデーション": "最小8文字、英数字混在",
    "説明": "パスワード"
  },
  "username": {
    "型": "string",
    "必須": true,
    "バリデーション": "3-50文字",
    "説明": "ユーザー名"
  }
}
```

**レスポンス**

- 成功時（201）

```json
{
  "data": {
    "user_id": "string",
    "email": "string",
    "username": "string",
    "created_at": "datetime"
  },
  "token": {
    "access_token": "string",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

## 2. ログイン

**概要**

- 説明：既存ユーザーの認証とトークン発行
- パス：`/api/v1/auth/login`
- メソッド：`POST`
- 認証要件：不要

**リクエスト**

```json
{
  "email": {
    "型": "string",
    "必須": true,
    "説明": "登録済みメールアドレス"
  },
  "password": {
    "型": "string",
    "必須": true,
    "説明": "パスワード"
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
    "username": "string"
  },
  "token": {
    "access_token": "string",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "string"
  }
}
```

## 3. ログアウト

**概要**

- 説明：ユーザーのログアウトとトークンの無効化
- パス：`/api/v1/auth/logout`
- メソッド：`POST`
- 認証要件：必要

**リクエスト**

- ヘッダーに有効なアクセストークンが必要

**レスポンス**

- 成功時（200）

```json
{
  "message": "正常にログアウトしました"
}
```

## 4. トークンリフレッシュ

**概要**

- 説明：リフレッシュトークンを使用した新規アクセストークンの発行
- パス：`/api/v1/auth/refresh`
- メソッド：`POST`
- 認証要件：不要（リフレッシュトークンが必要）

**リクエスト**

```json
{
  "refresh_token": {
    "型": "string",
    "必須": true,
    "説明": "有効なリフレッシュトークン"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "token": {
    "access_token": "string",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

## 共通エラーレスポンス

### 認証エラー（401）

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "認証に失敗しました",
    "details": {
      "reason": "無効なトークンまたは期限切れ"
    }
  }
}
```

### バリデーションエラー（422）

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力値が不正です",
    "details": {
      "field": ["エラーの詳細"]
    }
  }
}
```

## セキュリティ仕様

1. パスワードの要件

   - 最小 8 文字
   - 英大文字、小文字、数字を含む
   - 特殊文字を推奨

2. トークン仕様

   - アクセストークン有効期限：1 時間
   - リフレッシュトークン有効期限：30 日
   - JWT フォーマットを使用

3. レート制限
   - ログイン試行：5 回/分
   - サインアップ：3 回/分
   - その他のエンドポイント：60 回/分


