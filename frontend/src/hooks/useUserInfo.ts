import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "./useAuth"; // 既存の認証情報取得フック
import { config } from "../core/config";

export function useUserInfo() {
  const queryClient = useQueryClient();
  const { user } = useAuth();

  return useQuery({
    queryKey: ["userInfo"],
    queryFn: async () => {
      if (!user) throw new Error("未ログインです");
      const idToken = await user.getIdToken();
      const res = await fetch(`${config.api.baseUrl}/users/me`, {
        headers: {
          Authorization: `Bearer ${idToken}`,
          "Content-Type": "application/json",
        },
      });
      if (!res.ok) throw new Error("ユーザー情報の取得に失敗しました");
      const data = await res.json();
      // 必要ならここでsessionStorageにも保存
      sessionStorage.setItem("userInfo", JSON.stringify(data));
      return data;
    },
    staleTime: 1000 * 60 * 10, // 10分キャッシュ
    // cacheTime: 1000 * 60 * 60, // 1時間キャッシュ
    enabled: !!user, // userが取得できてからリクエスト
    initialData: () => {
      // sessionStorageにあれば初期値として使う
      const cached = sessionStorage.getItem("userInfo");
      return cached ? JSON.parse(cached) : undefined;
    },
  });
}
