import React from "react";
import { Box, Container, Paper, Typography, useTheme } from "@mui/material";
import { Outlet } from "react-router-dom";

const LoginLayout: React.FC = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: theme.palette.grey[50],
      }}
    >
      {/* ヘッダー部分 */}
      <Box
        component="header"
        sx={{
          py: 2,
          backgroundColor: theme.palette.primary.main,
          color: theme.palette.primary.contrastText,
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="h5" component="h1">
            サービス名
          </Typography>
        </Container>
      </Box>

      {/* メインコンテンツ */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          py: 4,
        }}
      >
        <Container component="main" maxWidth="xs">
          <Paper
            elevation={3}
            sx={{
              p: 4,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              borderRadius: 2,
            }}
          >
            <Outlet />
          </Paper>
        </Container>
      </Box>

      {/* フッター部分 */}
      <Box
        component="footer"
        sx={{
          py: 3,
          backgroundColor: theme.palette.grey[200],
          textAlign: "center",
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} サービス名. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default LoginLayout;
