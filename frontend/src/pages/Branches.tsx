import React from "react";
import { Typography, Box, CircularProgress, List } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { useBranches } from "../hooks/useBranches";
import { useUserInfo } from "../hooks/useUserInfo";
import BranchCard from "../components/common/Card/BranchCard";
import { UserInfo } from "../types"; // UserInfo型をインポート

const Branches: React.FC = () => {
  const navigate = useNavigate();
  const { company_id } = useParams<{ company_id: string }>();
  const {
    data: branches,
    isLoading: branchesLoading,
    error: branchesError,
  } = useBranches(company_id);
  const {
    data: userInfo,
    isLoading: userInfoLoading,
    error: userInfoError,
  } = useUserInfo();

  // ローディング状態のチェック
  if (branchesLoading || userInfoLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="50vh"
      >
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>データを読み込み中...</Typography>
      </Box>
    );
  }

  // エラー状態のチェック
  if (branchesError) {
    return (
      <Typography color="error">店舗データの取得に失敗しました</Typography>
    );
  }
  if (userInfoError) {
    return (
      <Typography color="error">ユーザー情報の取得に失敗しました</Typography>
    );
  }

  return (
    <DefaultLayout>
      <Box sx={{ maxWidth: 900, mx: "auto", mt: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ mt: -4 }}>
          店舗一覧
        </Typography>
        <List>
          {branches && branches.length > 0 ? (
            branches.map((branch: any) => (
              <BranchCard
                key={branch.id}
                branch={branch}
                userInfo={userInfo as UserInfo} // 型アサーションを追加
              />
            ))
          ) : (
            <Typography>店舗がありません</Typography>
          )}
        </List>
      </Box>
    </DefaultLayout>
  );
};

export default Branches;
