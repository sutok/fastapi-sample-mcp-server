import React from "react";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { Typography, Paper, Box } from "@mui/material";

const Dashboard: React.FC = () => {
  return (
    <DefaultLayout>
      <Typography variant="h4" gutterBottom>
        ダッシュボード
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
