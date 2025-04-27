import React from "react";
import { Box, Container, Paper, Typography, useTheme } from "@mui/material";
import { Outlet } from "react-router-dom";

export const UserLayout: React.FC = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: theme.palette.grey[100],
      }}
    >
      {/* ヘッダー部分 */}
      <Box
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
      <Container
        component="main"
        maxWidth="sm"
        sx={{
          mt: 4,
          mb: 4,
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            width: "100%",
            maxWidth: "sm",
          }}
        >
          <Outlet />
        </Paper>
      </Container>

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
