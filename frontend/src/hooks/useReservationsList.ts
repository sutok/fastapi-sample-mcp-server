import { useQuery } from "@tanstack/react-query";
import { auth } from "../firebase";
import { config } from "../core/config";
import { useParams } from "react-router-dom";
import { useUserInfo } from "./useUserInfo";

export const useReservationsList = (
  company_id?: string,
  branch_id?: string
) => {
  // ユーザー情報を取得
  const { data: userInfo, isLoading, error } = useUserInfo();
  // 空やnull/undefinedのものは除外してURLSearchParamsを作成
  const searchParams = new URLSearchParams();
  if (userInfo?.id) {
    searchParams.append("user_id", userInfo.id);
  }
  if (userInfo?.company_id) {
    searchParams.append("company_id", userInfo.company_id);
  }
  if (userInfo?.branch_id) {
    searchParams.append("branch_id", userInfo.branch_id);
  }
  const paramsString = searchParams.toString();

  return useQuery({
    queryKey: ["reservations", company_id, branch_id],
    queryFn: async () => {
      const currentUser = auth.currentUser;
      if (!currentUser) return [];
      const idToken = await currentUser.getIdToken();
      // console.log("idToken", idToken);

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
      return await response.json();
    },
    staleTime: 1000 * 60 * 5,
  });
};
