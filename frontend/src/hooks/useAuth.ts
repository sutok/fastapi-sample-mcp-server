import { useEffect, useState } from "react";
import { User, onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      // console.log(firebaseUser?.getIdToken());
      // ユーザー情報取得
      // const userInfo = await fetch(`${config.api.baseUrl}/users/me`, {
      //   headers: {
      //     Authorization: `Bearer ${idToken}`,
      //     "Content-Type": "application/json",
      //   },
      // });
      // const userInfoData = await userInfo.json();
      // const company_id = userInfoData.company_id;

      setUser(firebaseUser);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  return { user, loading };
}
