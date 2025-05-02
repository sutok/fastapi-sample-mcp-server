import { useState, useEffect } from "react";
import { auth } from "../firebase";
import { config } from "../core/config";

/**
 * 予約情報を表すインターフェース
 */
interface Reservation {
  id: string; // 予約ID
  number: number; // 予約番号
  status: "waiting" | "called" | "completed" | "cancelled"; // 予約状態
  created_at: string; // 予約作成日時
  store_id: string;
  store_name: string;
}

/**
 * 予約情報を管理するカスタムフック
 * @param storeId 店舗ID
 * @returns {Object} 予約情報、読み込み状態、予約作成関数、予約情報更新関数
 */
export const useReservation = (storeId: string | null) => {
  const [reservation, setReservation] = useState<Reservation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * 現在の予約情報を取得する
   */
  const fetchReservation = async () => {
    const currentUser = auth.currentUser;
    if (!currentUser || !storeId) {
      setLoading(false);
      return;
    }

    try {
      const idToken = await currentUser.getIdToken();
      // 指定された店舗の現在の予約を取得
      const response = await fetch(
        `${config.api.baseUrl}/reservations/current?store_id=${storeId}`,
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setReservation(data);
      setError(null);
    } catch (error: any) {
      console.error("予約情報の取得に失敗:", error);
      setError("予約情報の取得に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  /**
   * 新規予約を作成する
   * @returns {Promise<Reservation>} 作成された予約情報
   */
  const createReservation = async () => {
    const currentUser = auth.currentUser;
    if (!currentUser || !storeId) return;

    try {
      const idToken = await currentUser.getIdToken();
      // 新規予約をAPIに送信
      const response = await fetch(`${config.api.baseUrl}/reservations`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${idToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          store_id: storeId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setReservation(data);
      setError(null);
      return data;
    } catch (error: any) {
      console.error("予約の作成に失敗:", error);
      setError("予約の作成に失敗しました");
      throw error;
    }
  };

  // 店舗IDが変更されたら予約情報を再取得
  useEffect(() => {
    fetchReservation();
  }, [storeId]);

  return {
    reservation,
    loading,
    error,
    createReservation,
    refreshReservation: fetchReservation,
  };
};
