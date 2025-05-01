# 予約管理 API 仕様書

## 1. 予約作成

**概要**

- 説明：新規予約の作成
- パス：`/api/v1/reservations`
- メソッド：`POST`
- 認証要件：必要

**リクエスト**

```json
{
  "reservation_date": {
    "型": "string (ISO8601)",
    "必須": true,
    "バリデーション": "未来の日付",
    "説明": "予約日"
  },
  "reservation_time": {
    "型": "string",
    "必須": true,
    "バリデーション": "HH:mm形式、30分単位",
    "説明": "予約時間枠"
  },
  "notes": {
    "型": "string",
    "必須": false,
    "バリデーション": "最大500文字",
    "説明": "備考"
  }
}
```

**レスポンス**

- 成功時（201）

```json
{
  "data": {
    "id": "string",
    "user_id": "string",
    "reception_number": "integer",
    "reservation_date": "string (ISO8601)",
    "reservation_time": "string",
    "notes": "string",
    "status": "confirmed",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

## 2. 予約一覧取得

**概要**

- 説明：ユーザーの予約一覧を取得
- パス：`/api/v1/reservations`
- メソッド：`GET`
- 認証要件：必要

**リクエスト**

- クエリパラメータ

```json
{
  "status": {
    "型": "string",
    "必須": false,
    "許可値": ["confirmed", "cancelled", "completed", "all"],
    "デフォルト": "confirmed",
    "説明": "予約ステータス"
  },
  "from_date": {
    "型": "string (ISO8601)",
    "必須": false,
    "説明": "検索開始日"
  },
  "to_date": {
    "型": "string (ISO8601)",
    "必須": false,
    "説明": "検索終了日"
  },
  "page": {
    "型": "integer",
    "必須": false,
    "デフォルト": 1,
    "説明": "ページ番号"
  },
  "per_page": {
    "型": "integer",
    "必須": false,
    "デフォルト": 20,
    "バリデーション": "最大50",
    "説明": "1ページあたりの表示件数"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": [
    {
      "reservation_id": "string",
      "date": "string (ISO8601)",
      "time_slot": "string",
      "duration": "integer",
      "number_of_people": "integer",
      "status": "string",
      "notes": "string",
      "created_at": "datetime"
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "per_page": 20
  }
}
```

## 3. 予約詳細取得

**概要**

- 説明：特定の予約詳細を取得
- パス：`/api/v1/reservations/{reservation_id}`
- メソッド：`GET`
- 認証要件：必要

**リクエスト**

- パスパラメータのみ

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "reservation_id": "string",
    "user_id": "string",
    "status": "string",
    "date": "string (ISO8601)",
    "time_slot": "string",
    "duration": "integer",
    "number_of_people": "integer",
    "notes": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "cancellation": {
      "cancelled_at": "datetime",
      "reason": "string"
    }
  }
}
```

## 4. 予約更新

**概要**

- 説明：既存の予約を更新
- パス：`/api/v1/reservations/{reservation_id}`
- メソッド：`PATCH`
- 認証要件：必要

**リクエスト**

```json
{
  "date": {
    "型": "string (ISO8601)",
    "必須": false,
    "バリデーション": "未来の日付",
    "説明": "予約日"
  },
  "time_slot": {
    "型": "string",
    "必須": false,
    "バリデーション": "HH:mm形式",
    "説明": "予約時間枠"
  },
  "duration": {
    "型": "integer",
    "必須": false,
    "バリデーション": "30分単位、最大180分",
    "説明": "予約時間（分）"
  },
  "number_of_people": {
    "型": "integer",
    "必須": false,
    "バリデーション": "1以上",
    "説明": "予約人数"
  },
  "notes": {
    "型": "string",
    "必須": false,
    "バリデーション": "最大500文字",
    "説明": "備考"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "reservation_id": "string",
    "status": "confirmed",
    "date": "string (ISO8601)",
    "time_slot": "string",
    "duration": "integer",
    "number_of_people": "integer",
    "notes": "string",
    "updated_at": "datetime"
  }
}
```

## 5. 予約キャンセル

**概要**

- 説明：予約をキャンセル
- パス：`/api/v1/reservations/{reservation_id}/cancel`
- メソッド：`POST`
- 認証要件：必要

**リクエスト**

```json
{
  "reason": {
    "型": "string",
    "必須": false,
    "バリデーション": "最大500文字",
    "説明": "キャンセル理由"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "reservation_id": "string",
    "status": "cancelled",
    "cancelled_at": "datetime",
    "reason": "string"
  }
}
```

## 6. 空き状況確認

**概要**

- 説明：指定日の予約可能な時間枠を取得
- パス：`/api/v1/reservations/availability`
- メソッド：`GET`
- 認証要件：不要

**リクエスト**

- クエリパラメータ

```json
{
  "date": {
    "型": "string (ISO8601)",
    "必須": true,
    "説明": "確認したい日付"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "date": "string (ISO8601)",
    "target_date": "2024-07-01",
    "available_slots": [
      {"time":"09:00", "is_resarved": true/false},
      {"time":"09:30", "is_resarved": true/false},
      {"time":"10:00", "is_resarved": true/false},
      ...
    ],
    "is_open": true
  }
}
```

## 7. 現在の呼び出し番号確認

**概要**

- 説明：現在対応中の予約番号と自分の順番を確認
- パス：`/api/v1/reservations/current-status`
- メソッド：`GET`
- 認証要件：必要

**リクエスト**

- クエリパラメータ

```json
{
  "reservation_id": {
    "型": "string",
    "必須": false,
    "説明": "特定の予約IDの順番を確認する場合"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "current_number": {
      "reservation_id": "string",
      "number": "integer",
      "estimated_start_time": "string (HH:mm)",
      "status": "in_progress"
    },
    "your_reservation": {
      "reservation_id": "string",
      "number": "integer",
      "position_in_queue": "integer",
      "estimated_wait_time": "integer", // 分単位
      "estimated_start_time": "string (HH:mm)"
    },
    "queue_summary": {
      "total_waiting": "integer",
      "average_wait_time": "integer" // 分単位
    },
    "last_updated_at": "datetime"
  }
}
```

## 8. 順番表示板用エンドポイント

**概要**

- 説明：順番表示板用の現在の呼び出し状況を取得
- パス：`/api/v1/reservations/display-board`
- メソッド：`GET`
- 認証要件：不要（表示用トークンが必要）

**リクエスト**

- ヘッダーパラメータ

```json
{
  "X-Display-Token": {
    "型": "string",
    "必須": true,
    "説明": "表示板用の認証トークン"
  }
}
```

**レスポンス**

- 成功時（200）

```json
{
  "data": {
    "now_serving": {
      "number": "integer",
      "time_slot": "string (HH:mm)"
    },
    "next_in_line": [
      {
        "number": "integer",
        "estimated_start_time": "string (HH:mm)"
      }
    ],
    "announcements": [
      {
        "message": "string",
        "priority": "normal/high"
      }
    ],
    "last_updated_at": "datetime"
  }
}
```

## エラーレスポンス

### 予約が見つからない（404）

```json
{
  "error": {
    "code": "RESERVATION_NOT_FOUND",
    "message": "指定された予約が見つかりません",
    "details": {
      "reservation_id": "string"
    }
  }
}
```

### 無効な表示トークン（401）

```json
{
  "error": {
    "code": "INVALID_DISPLAY_TOKEN",
    "message": "無効な表示用トークンです"
  }
}
```

## ビジネスルール

1. 予約制限

   - 1 ユーザーあたりの同時予約数：最大 5 件（前の予約が受付済みでないと次の予約は許可されない）
   - 予約可能期間：1 日先まで。（0 の場合は当日のみ）
   - キャンセル可能期限：予約時間の 24 時間前まで（0 の場合は 30 分前まで。キャンセル許可されない場合は連絡先を表示）

2. 時間枠

   - 営業時間：10:00-22:00
   - 時間枠単位：30 分
   - 最大予約時間：3 時間
   - 最小予約時間：30 分

3. キャンセルポリシー

   - 24 時間前まで：無料
   - 24 時間以内：キャンセル料発生
   - 当日キャンセル：全額

4. 順番表示

   - 予約時間枠ごとに番号を割り当て
   - 番号は日付ごとに分ける
   - 予約番号は 4 桁で表示（例：0001）

5. 待ち時間計算

   - 直近の実績データに基づく待ち時間の計算（予約 1 件にたいしての想定時間を設定している場合のみ）
   - 予約時間枠と実際の所要時間の差を考慮
   - 1 予約を 5 分位で待ち時間を更新

6. 表示制限
   - 次の呼び出し予定は最大 5 件まで表示
   - 待ち時間が 60 分を超える場合は概算で表示

## レート制限

- 予約作成：10 回/時
- 予約更新：20 回/時
- 空き状況確認：60 回/時
- その他エンドポイント：30 回/時

## WebSocket 対応（オプション）

- エンドポイント：`ws://api/v1/reservations/status-stream`
- リアルタイムでの順番更新通知
- クライアントは認証後に接続可能
