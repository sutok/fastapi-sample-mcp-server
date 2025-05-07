import React from "react";
import { Typography, Box, CircularProgress } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import DefaultLayout from "../components/layouts/DefaultLayout";
// 店舗一覧取得用のカスタムフック（仮定）
import { useBranches } from "../hooks/useBranches";
import BranchCard from "../components/common/Card/BranchCard";
// import { Branch } from "../types";

const Branches: React.FC = () => {
  const navigate = useNavigate();
  // URLパラメータからcompany_idを取得
  const { company_id } = useParams<{ company_id: string }>();
  // Branches一覧をキャッシュから取得
  const { data: branches, isLoading, error } = useBranches(company_id);
  if (isLoading) return <div>読み込み中...</div>;
  if (error) return <div>エラー: {error.message}</div>;
  // 入力値でフィルタ
  // const filteredBranches = branches
  //   ? branches.filter((branch) =>
  //       branch.id.toLowerCase().includes(search.toLowerCase())
  //     )
  //   : [];

  if (isLoading) {
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
  console.log(branches);

  return (
    <DefaultLayout>
      <Box sx={{ maxWidth: 900, mx: "auto", mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          店舗一覧
        </Typography>
        {/* <input
          type="text"
          placeholder="店舗名で検索"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ marginBottom: "1em" }}
        /> */}
        <ul>
          {branches && branches.length > 0 ? (
            branches.map((branch) => (
              <li key={branch.id}>
                <BranchCard key={branch.id} branch={branch} />
              </li>
            ))
          ) : (
            <li>店舗がありません</li>
          )}
        </ul>
      </Box>
    </DefaultLayout>
  );
};

export default Branches;
