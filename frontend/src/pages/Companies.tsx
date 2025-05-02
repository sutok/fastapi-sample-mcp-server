import React from "react";
import {
  Typography,
  Paper,
  Box,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import { useCompanies } from "../hooks/useCompanies";

const Companies: React.FC = () => {
  const { companies, loading, error } = useCompanies();

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="50vh"
      >
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>企業データを読み込み中...</Typography>
      </Box>
    );
  }
  console.log(companies);

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        企業一覧
      </Typography>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {companies.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: "center" }}>
          <Typography>企業が登録されていません</Typography>
        </Paper>
      ) : (
        <Paper>
          <List>
            {companies.map((company) => (
              <ListItem key={company.id}>
                <ListItemText
                  primary={company.company_name}
                  secondary={company.address || "説明なし"}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
};

export default Companies;
