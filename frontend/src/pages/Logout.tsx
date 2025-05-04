import { useEffect } from "react";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useNavigate } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";

export default function Logout() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  useEffect(() => {
    const doLogout = async () => {
      await signOut(auth);
      queryClient.clear();
      sessionStorage.clear();
      navigate("/login");
    };
    doLogout();
  }, [navigate, queryClient]);

  return null; // 何も表示しない
}
