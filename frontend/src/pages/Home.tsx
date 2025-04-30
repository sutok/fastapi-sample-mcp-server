import React from "react";
import { Container, Typography, Box, Button, Grid, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          予約管理システム
        </Typography>

        <Grid container spacing={3} sx={{ mt: 4 }}>
          <Grid item xs={12} md={6}>
            <Paper
              sx={{
                p: 3,
                display: "flex",
                flexDirection: "column",
                height: "100%",
                minHeight: "200px",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Typography variant="h5" gutterBottom>
                企業管理
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                企業情報の登録・編集・削除を行います
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate("/companies")}
              >
                企業一覧へ
              </Button>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper
              sx={{
                p: 3,
                display: "flex",
                flexDirection: "column",
                height: "100%",
                minHeight: "200px",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Typography variant="h5" gutterBottom>
                店舗管理
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                店舗情報の登録・編集・削除を行います
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate("/stores")}
              >
                店舗一覧へ
              </Button>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper
              sx={{
                p: 3,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                mt: 2,
              }}
            >
              <Typography variant="h5" gutterBottom>
                予約管理
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                予約の確認・管理を行います
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate("/reservations")}
              >
                予約一覧へ
              </Button>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Home;
