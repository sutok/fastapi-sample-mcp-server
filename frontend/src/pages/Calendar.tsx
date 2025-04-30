import React from "react";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { Typography, Paper, Box } from "@mui/material";

const Calendar: React.FC = () => {
  return (
    <DefaultLayout>
      <Typography variant="h4" gutterBottom>
        カレンダー
      </Typography>
      <Paper sx={{ p: 2 }}>
        <Box>
          <Typography>カレンダーの内容をここに表示</Typography>
        </Box>
      </Paper>
    </DefaultLayout>
  );
};

export default Calendar;
