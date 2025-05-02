import React from "react";
import {
  Typography,
  Paper,
  Box,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { useCompanies } from "../hooks/useCompanies";
import DefaultLayout from "../components/layouts/DefaultLayout";

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
    <DefaultLayout>
      <Box sx={{ maxWidth: 900, mx: "auto", mt: 4 }}>
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
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>企業名</TableCell>
                  <TableCell>住所</TableCell>
                  <TableCell>TEL</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {companies.map((company) => (
                  <TableRow key={company.id}>
                    <TableCell>{company.company_name}</TableCell>
                    <TableCell>{company.address || "説明なし"}</TableCell>
                    <TableCell>{company.phone_number || ""}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Box>
    </DefaultLayout>
  );
};

export default Companies;
