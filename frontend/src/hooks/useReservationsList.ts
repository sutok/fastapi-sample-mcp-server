import { useQuery, useQueryClient } from "@tanstack/react-query";
import { auth } from "../firebase";
import { config } from "../core/config";
import { useUserInfo } from "./useUserInfo";
import { Reservation } from "../types";

export const useReservationsList = (
  company_id?: string,
  branch_id?: string
) => {
  const { data: userInfo } = useUserInfo();
  const currentUser = auth.currentUser;
  const queryClient = useQueryClient();

  return useQuery<Reservation[], Error>({
    queryKey: ["reservations", company_id, branch_id],
    queryFn: async (): Promise<Reservation[]> => {
      if (!currentUser) return [];

      // クエリパラメータの構築
      const searchParams = new URLSearchParams();
      if (company_id) {
        searchParams.append("company_id", company_id);
      }
      if (branch_id) {
        searchParams.append("branch_id", branch_id);
      }
      if (userInfo?.id) {
        searchParams.append("user_id", userInfo.id);
      }
      const today = new Date().toISOString().split("T")[0];
      searchParams.append("target_date", today);
      searchParams.append("status", "accepted,calling");
      const paramsString = searchParams.toString();

      const idToken = await currentUser.getIdToken();
      const response = await fetch(
        `${config.api.baseUrl}/reservations?${paramsString}`,
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) throw new Error("予約一覧の取得に失敗しました");
      const data = (await response.json()) as Reservation[];

      // 重複を除去
      const uniqueData: Reservation[] = Array.from(
        new Map(data.map((item) => [item.id, item])).values()
      );

      // キャッシュを更新
      queryClient.setQueryData(
        ["reservations", company_id, branch_id],
        uniqueData
      );

      return uniqueData;
    },
    enabled: !!currentUser && !!userInfo,
    staleTime: 1000 * 60 * 5, // 5分間はデータを新鮮とみなす
    gcTime: 1000 * 60 * 10, // 10分間キャッシュを保持
  });
};
