# Firebase プロジェクトセットアップ手順

## 1. プロジェクト作成

1. Firebase Console にアクセス

   - https://console.firebase.google.com/

2. プロジェクトを作成
   - プロジェクト名: `sample-fastapi`
   - Google Analytics: 有効化
   - リージョン: `asia-northeast1`（東京）

## 2. 認証設定（Authentication）

### 認証方式の有効化

1. メール/パスワード認証

   - 有効化
   - メールリンクによるパスワードレス認証: 無効

2. 追加設定
   ```json
   {
     "passwordPolicy": {
       "minLength": 8,
       "requireUppercase": true,
       "requireLowercase": true,
       "requireNumber": true,
       "requireSpecialCharacter": true
     },
     "emailVerification": {
       "required": true,
       "templateLanguage": "ja"
     }
   }
   ```

### メールテンプレートのカスタマイズ

1. 確認メール
2. パスワードリセット
3. メールアドレス変更

## 3. Firestore 設定

### データベース作成

1. 本番環境

   - ロケーション: `asia-northeast1`
   - 本番モード

2. セキュリティルール

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザードキュメント
    match /users/{userId} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if request.auth != null && request.auth.uid == userId;
    }

    // 予約ドキュメント
    match /reservations/{reservationId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null &&
        resource.data.userId == request.auth.uid;
    }
  }
}
```

### インデックス設定

```json
{
  "indexes": [
    {
      "collectionGroup": "reservations",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "userId",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "date",
          "order": "ASCENDING"
        }
      ]
    },
    {
      "collectionGroup": "reservations",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "date",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "status",
          "order": "ASCENDING"
        }
      ]
    }
  ]
}
```

## 4. Firebase Admin SDK 設定

### サービスアカウントの作成

1. プロジェクト設定 > サービスアカウント
2. 新しい秘密鍵の生成
3. JSON ファイルのダウンロード

### 環境変数の設定

```env
FIREBASE_PROJECT_ID=sample-fastapi
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@sample-fastapi.iam.gserviceaccount.com
```

## 5. Firebase Hosting 設定（オプション）

### 初期設定

```json
{
  "hosting": {
    "public": "public",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "/api/**",
        "run": {
          "serviceId": "fastapi-service",
          "region": "asia-northeast1"
        }
      },
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

## 6. 開発環境用の設定

### Firebase Emulator Suite

1. インストール

```bash
npm install -g firebase-tools
```

2. 必要なエミュレータの設定

```json
{
  "emulators": {
    "auth": {
      "port": 9099
    },
    "firestore": {
      "port": 8080
    },
    "hosting": {
      "port": 5000
    },
    "ui": {
      "enabled": true
    }
  }
}
```

### 環境変数（開発用）

```env
FIREBASE_AUTH_EMULATOR_HOST=localhost:9099
FIRESTORE_EMULATOR_HOST=localhost:8080
```

## 7. セキュリティ設定

### API 制限

1. API キーの制限

   - 許可するドメイン設定
   - 使用量制限の設定

2. OAuth 同意画面
   - アプリ名
   - ロゴ
   - 利用規約 URL
   - プライバシーポリシー URL

### モニタリング設定

1. Cloud Monitoring の有効化
2. アラート設定
   - 認証失敗回数
   - API リクエスト数
   - エラー率

## 8. バックアップ設定

### Firestore バックアップ

1. 自動バックアップの設定
   - 頻度: 毎日
   - 保持期間: 30 日
   - 保存先: Cloud Storage


