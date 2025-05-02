import { useState, useEffect } from "react";
import { config } from "../core/config";
import { Company } from "../types";
import { auth } from "../firebase";
import { User, onAuthStateChanged } from "firebase/auth";
/**
 * 企業一覧を管理するカスタムフック
 */
export const useCompanies = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    if (authLoading) return;
    if (!user) return;

    const fetchCompanies = async () => {
      setLoading(true);
      try {
        const idToken = await user.getIdToken();
        const response = await fetch(`${config.api.baseUrl}/companies/`, {
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
        console.log(data);
        setCompanies(data);
        setError(null);
      } catch (err: any) {
        setError("企業データの取得に失敗しました");
      } finally {
        setLoading(false);
      }
    };
    fetchCompanies();
  }, [user, authLoading]);

  return { companies, loading, error };
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
