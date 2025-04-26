import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { Button } from "@mui/material";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";

export default function Dashboard() {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;

  const handleLogout = async () => {
    await signOut(auth);
    // サインアウト後は自動的にuseAuthのuserがnullになり、ログイン画面へリダイレクトされます
  };

  return (
    <div>
      <h2>ダッシュボード</h2>
      <p>ようこそ、{user.email} さん！</p>
      <Button
        variant="outlined"
        color="secondary"
        onClick={handleLogout}
        sx={{ mt: 2 }}
      >
        ログアウト
      </Button>
    </div>
  );
}
