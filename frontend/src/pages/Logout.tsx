import { useEffect } from "react";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    const doLogout = async () => {
      await signOut(auth);
      navigate("/login");
    };
    doLogout();
  }, [navigate]);

  return null; // 何も表示しない
}
