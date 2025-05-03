import { useState, useEffect } from "react";
import { config } from "../core/config";
import { Branch } from "../types";
import { auth } from "../firebase";
import { User, onAuthStateChanged } from "firebase/auth";
/**
 * 企業一覧を管理するカスタムフック
 */
export const useBranches = () => {
  const [branches, setBranches] = useState<Branch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    if (authLoading) return;
    if (!user) return;

    const fetchBranches = async () => {
      setLoading(true);
      try {
        const idToken = await user.getIdToken();
        const response = await fetch(`${config.api.baseUrl}/stores/`, {
          headers: {
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        });
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
  }, [user, authLoading]);

  return { branches, loading, error };
};

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  return { user, loading };
}
