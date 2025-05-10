import { useState, useEffect } from "react";
import { auth } from "../firebase";
import axios from "axios";
import { config } from "../core/config";

interface BusinessHours {
  morning_start: string;
  morning_end: string;
  afternoon_start: string;
  afternoon_end: string;
}

interface WaitingStatus {
  current_time: string;
  business_hours: BusinessHours;
  current_number: number | null;
  latest_reception_number: number | null;
  waiting_count: number;
}

export const useWaitingStatus = (
  companyId: string | undefined,
  branchId: string | undefined
) => {
  const [status, setStatus] = useState<WaitingStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = async () => {
    // companyIdまたはbranchIdが未定義の場合は何もしない
    if (!companyId || !branchId) {
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      // 現在のユーザーのIDトークンを取得
      const user = auth.currentUser;
      if (!user) {
        // 認証情報が無ければログアウト画面にリダイレクト
        navigate("/logout");
        return;
        // throw new Error("ユーザーが認証されていません");
      }
      const token = await user.getIdToken();

      const response = await axios.get<WaitingStatus>(
        `${config.api.baseUrl}/reservations/${companyId}/${branchId}/summary`,
        {
          headers: {
            Authorization: `Bearer ${token}`, // ベアラートークンを付与
          },
        }
      );
      setStatus(response.data);
    } catch (err) {
      setError("予約状況の取得に失敗しました");
      console.error("Error fetching waiting status:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    // 1分ごとに更新
    const interval = setInterval(fetchStatus, 60000);
    return () => clearInterval(interval);
  }, [companyId, branchId]);

  return { status, isLoading, error, refetch: fetchStatus };
};
