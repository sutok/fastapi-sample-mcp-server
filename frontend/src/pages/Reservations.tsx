import React from "react";
import { Typography } from "@mui/material";
import { useParams } from "react-router-dom";
import { useUserInfo } from "../hooks/useUserInfo";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { useAuth } from "../hooks/useAuth";
// import { useReservations } from "../hooks/useReservations";
import ReservationCard from "../components/common/Card/ReservationWaitingStatusCard";
import { useReservationsList } from "../hooks/useReservationsList";
import { useBranches } from "../hooks/useBranches";
import ReservationWaitingStatusCard from "../components/common/Card/ReservationWaitingStatusCard";

const Reservations: React.FC = () => {
  // URLパラメータからcompany_idとbranch_idを取得
  const { company_id, branch_id } = useParams<{
    company_id: string;
    branch_id: string;
  }>();
  // ユーザー情報を取得
  const {
    data: userInfo,
    isLoading: userInfoLoading,
    error: userInfoError,
  } = useUserInfo();
  // 店舗情報取得
  const {
    data: branches,
    isLoading: branchLoading,
    error: branchError,
  } = useBranches(company_id);
  // 予約一覧を取得
  const {
    data: reservations,
    isLoading: reservationsLoading,
    error: reservationsError,
  } = useReservationsList(company_id, branch_id);

  if (userInfoLoading || reservationsLoading || branchLoading)
    return <div>読み込み中...</div>;
  if (userInfoError)
    return <div>ユーザー情報取得エラー: {userInfoError.message}</div>;
  if (reservationsError)
    return <div>予約一覧取得エラー: {reservationsError.message}</div>;
  if (branchError) return <div>店舗情報取得エラー: {branchError.message}</div>;
  // debug--------------------------------
  const branch = branches?.find((branch) => branch.id === branch_id);
  // console.log("branches", branches);
  // debug--------------------------------
  console.log("branch", branch);
  console.log("reservations", reservations);
  // debug--------------------------------

  return (
    <DefaultLayout>
      <Typography variant="h4" gutterBottom sx={{ mt: -4 }}>
        <div style={{ maxWidth: 900, margin: "40px auto" }}>
          {/* // 予約状況-------------------------------- */}
          {company_id && branch_id && (
            <ReservationWaitingStatusCard
              companyId={company_id}
              branchId={branch_id}
              reservation={reservations?.[0]}
            />
          )}
          {/* // 予約状況-------------------------------- */}
          {/* // debug-------------------------------- */}
          <p>company_id: {company_id}</p>
          <p>branch_id: {branch_id}</p>
          {/* <p>target_date: {target_date}</p> */}
          {/* // debug-------------------------------- */}
        </div>
      </Typography>
    </DefaultLayout>
  );
};

export default Reservations;
