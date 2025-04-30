import React from "react";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { Typography, Paper, Box } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const Dashboard: React.FC = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !user) {
      navigate("/login");
    }
  }, [user, loading, navigate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <DefaultLayout>
      <Typography variant="h4" gutterBottom>
        待ち状況
      </Typography>
      <Paper sx={{ p: 2, mt: 2 }}>
        <Box>
          <Typography>ここにダッシュボードの内容を表示します。</Typography>
        </Box>
      </Paper>
    </DefaultLayout>
  );
};

export default Dashboard;
