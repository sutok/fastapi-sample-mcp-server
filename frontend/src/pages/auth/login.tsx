import { useState } from "react";
import { Box, Typography, Paper } from "@mui/material";
import { Input } from "@/components/common/Input";
import { Button } from "@/components/common/Button";
import { Layout } from "@/components/common/Layout";
import { useAuth } from "@/hooks/useAuth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
  };

  return (
    <Layout>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "calc(100vh - 64px)",
        }}
      >
        <Paper sx={{ p: 4, maxWidth: 400, width: "100%" }}>
          <Typography variant="h5" sx={{ mb: 3 }}>
            ログイン
          </Typography>
          <form onSubmit={handleSubmit}>
            <Box sx={{ mb: 2 }}>
              <Input
                label="メールアドレス"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Box>
            <Box sx={{ mb: 3 }}>
              <Input
                label="パスワード"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Box>
            <Button
              variant="primary"
              type="submit"
              fullWidth
              disabled={loading}
            >
              ログイン
            </Button>
          </form>
        </Paper>
      </Box>
    </Layout>
  );
}
