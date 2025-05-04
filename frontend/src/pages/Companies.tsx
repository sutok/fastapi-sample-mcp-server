import React, { useState, useMemo, useEffect } from "react";
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
import { useNavigate } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import { config } from "../core/config";
import { useAuth } from "../hooks/useAuth";

const Companies: React.FC = () => {
  // ユーザー情報取得用のクエリクライアントを取得
  const queryClient = useQueryClient();
  // Firebase認証ユーザーを取得
  const { user } = useAuth();
  // userInfoのキャッシュがあれば初期値としてセット
  const [cachedUserInfo, setCachedUserInfo] = useState(() =>
    queryClient.getQueryData(["userInfo"])
  );
  // 企業一覧データ取得用カスタムフック
  const { companies, loading, error } = useCompanies();
  // 検索ワードの状態
  const [search, setSearch] = useState("");
  // ページ遷移用
  const navigate = useNavigate();

  // userInfoがキャッシュに無い場合はAPIから取得し、キャッシュに保存
  useEffect(() => {
    const fetchAndCacheUserInfo = async () => {
      if (!cachedUserInfo && user) {
        const idToken = await user.getIdToken();
        const res = await fetch(`${config.api.baseUrl}/users/me`, {
          headers: {
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        });
        if (res.ok) {
          const data = await res.json();
          // 取得したユーザー情報をキャッシュとstateに保存
          queryClient.setQueryData(["userInfo"], data);
          setCachedUserInfo(data);
        } else {
          setCachedUserInfo(undefined);
        }
      }
    };
    fetchAndCacheUserInfo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, cachedUserInfo]);

  // userInfoのキャッシュ内容をコンソールに出力（デバッグ用）
  useEffect(() => {
    // console.log("cachedUserInfo", cachedUserInfo);
  }, [cachedUserInfo]);

  // 検索ワードに応じて企業一覧をフィルタリング
  const filteredCompanies = useMemo(() => {
    if (!search) return companies;
    return companies.filter(
      (company) =>
        company.company_name.toLowerCase().includes(search.toLowerCase()) ||
        (company.address &&
          company.address.toLowerCase().includes(search.toLowerCase())) ||
        (company.phone_number && company.phone_number.includes(search))
    );
  }, [companies, search]);

  // 企業データ取得中のローディング表示
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

  // 企業一覧の表示
  return (
    <DefaultLayout>
      <Box sx={{ maxWidth: 900, mx: "auto", mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          企業一覧
        </Typography>
        {/* 検索ボックス */}
        <Box sx={{ mb: 2 }}>
          <input
            type="text"
            placeholder="フリーワード検索"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: "100%", padding: 8, fontSize: 16 }}
          />
        </Box>
        {/* エラー表示 */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        {/* 企業が0件の場合の表示 */}
        {filteredCompanies.length === 0 ? (
          <Paper sx={{ p: 3, textAlign: "center" }}>
            <Typography>企業が登録されていません</Typography>
          </Paper>
        ) : (
          // 企業一覧テーブル
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
                {filteredCompanies.map((company) => (
                  <TableRow key={company.id} hover>
                    <TableCell>
                      <span
                        style={{
                          color: "#1976d2",
                          cursor: "pointer",
                          textDecoration: "underline",
                        }}
                        onClick={() =>
                          navigate(`/company/${company.id}/branches`)
                        }
                      >
                        {company.company_name}
                      </span>
                    </TableCell>
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
