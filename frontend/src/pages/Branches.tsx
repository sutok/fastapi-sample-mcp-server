import React, { useState, useMemo } from "react";
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
import { useNavigate, useParams } from "react-router-dom";
import DefaultLayout from "../components/layouts/DefaultLayout";
// 店舗一覧取得用のカスタムフック（仮定）
import { useBranches } from "../hooks/useBranches";
import { Branch } from "../types";

const Branches: React.FC = () => {
  // URLパラメータからcompany_idを取得
  const { company_id } = useParams<{ company_id: string }>();
  // company_idをuseBranchesに渡す
  const { branches, loading, error } = useBranches(company_id);
  console.log("branches", branches);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  const filteredBranches = useMemo(() => {
    if (!search) return branches;
    return branches.filter(
      (branch: Branch) =>
        branch.branch_name.toLowerCase().includes(search.toLowerCase()) ||
        (branch.address &&
          branch.address.toLowerCase().includes(search.toLowerCase())) ||
        (branch.phone_number && branch.phone_number.includes(search))
    );
  }, [branches, search]);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="50vh"
      >
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>店舗データを読み込み中...</Typography>
      </Box>
    );
  }

  return (
    <DefaultLayout>
      <Box sx={{ maxWidth: 900, mx: "auto", mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          店舗一覧
        </Typography>
        <Box sx={{ mb: 2 }}>
          <input
            type="text"
            placeholder="フリーワード検索"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: "100%", padding: 8, fontSize: 16 }}
          />
        </Box>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        {filteredBranches.length === 0 ? (
          <Paper sx={{ p: 3, textAlign: "center" }}>
            <Typography>店舗が登録されていません</Typography>
          </Paper>
        ) : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>店舗名</TableCell>
                  <TableCell>住所</TableCell>
                  <TableCell>TEL</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredBranches.map((branch: Branch) => (
                  <TableRow
                    key={branch.id}
                    hover
                    style={{
                      color: "#1976d2",
                      cursor: "pointer",
                      textDecoration: "underline",
                    }}
                    onClick={() =>
                      navigate(
                        `/company/${company_id}/branches/${branch.id}/reservations`
                      )
                    }
                  >
                    <TableCell>{branch.branch_name}</TableCell>
                    <TableCell>{branch.address || "説明なし"}</TableCell>
                    <TableCell>{branch.phone_number || ""}</TableCell>
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

export default Branches;
