import { useState, useEffect } from "react";
import { config } from "../core/config";
import { Branch } from "../types";
import { auth } from "../firebase";
import { User, onAuthStateChanged } from "firebase/auth";
import { useAuth } from "./useAuth";

/**
 * 企業一覧を管理するカスタムフック
 */
export const useBranches = (company_id?: string) => {
  const [branches, setBranches] = useState<Branch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    if (authLoading) return;
    if (!user) return;
    if (!company_id) return;

    const fetchBranches = async () => {
      setLoading(true);
      try {
        const idToken = await user.getIdToken();
        // 店舗一覧取得
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
          throw new Error(
            `企業データの取得に失敗しました (${response.status})`
          );
        }
        const data = await response.json();
        setBranches(data);
        setError(null);
      } catch (err: any) {
        setError("企業データの取得に失敗しました");
      } finally {
        setLoading(false);
      }
    };
    fetchBranches();
  }, [user, authLoading, company_id]);

  return { branches, loading, error };
};
