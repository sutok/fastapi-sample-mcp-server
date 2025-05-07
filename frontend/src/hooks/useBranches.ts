import { useQuery } from "@tanstack/react-query";
import { config } from "../core/config";
import { Branch } from "../types";
import { useAuth } from "./useAuth";

/**
 * 店舗一覧を管理するカスタムフック（react-query版）
 */
export const useBranches = (company_id?: string) => {
  const { user, loading: authLoading } = useAuth();

  return useQuery<Branch[], Error>({
    queryKey: ["branches", company_id],
    queryFn: async () => {
      if (authLoading || !user || !company_id) return [];
      const idToken = await user.getIdToken();
      const response = await fetch(
        `${config.api.baseUrl}/branches/?company_id=${company_id}`,
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`店舗データの取得に失敗しました (${response.status})`);
      }
      return await response.json();
    },
    enabled: !authLoading && !!user && !!company_id,
    staleTime: 1000 * 60 * 10, // 10分キャッシュ
  });
};
