import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
} from "@mui/material";
import { useWaitingStatus } from "../../../hooks/useWaitingStatus";
import { Reservation, UserInfo } from "../../../types";

interface ReservationWaitingStatusCardProps {
  companyId: string;
  branchId: string;
  reservations: Reservation[];
  userInfo: UserInfo;
}

export const ReservationWaitingStatusCard: React.FC<
  ReservationWaitingStatusCardProps
> = ({ companyId, branchId, reservations, userInfo }) => {
  const { status, isLoading, error } = useWaitingStatus(companyId, branchId);

  // 予約の中で最も大きい受付番号を取得
  const latestReservation = reservations?.[0];

  // 予約の中で最も小さい受付番号を取得
  const callingReservation = reservations
    .filter((reservation) => reservation.status === "calling")
    .sort((a, b) => b.reception_number - a.reception_number)[0];

  // ユーザーの予約を取得
  const userReservation = reservations.find(
    (reservation) => reservation.user_id === userInfo.id
  );

  if (isLoading) {
    return (
      <Card sx={{ minWidth: 275, m: 2 }}>
        <CardContent sx={{ display: "flex", justifyContent: "center", p: 3 }}>
          <CircularProgress />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ minWidth: 275, m: 2 }}>
        <CardContent>
          <Typography color="error">{error}</Typography>
        </CardContent>
      </Card>
    );
  }

  if (!status) {
    return null;
  }

  const formatTime = (timeStr: string) => {
    return timeStr.replace(":", "時") + "分";
  };

  return (
    <Card sx={{ minWidth: 275, m: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div" gutterBottom>
          現在の予約状況
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" color="text.secondary">
            営業時間
          </Typography>
          <Typography variant="body2">
            午前の部: {formatTime(status.business_hours.morning_start)} -{" "}
            {formatTime(status.business_hours.morning_end)}
          </Typography>
          <Typography variant="body2">
            午後の部: {formatTime(status.business_hours.afternoon_start)} -{" "}
            {formatTime(status.business_hours.afternoon_end)}
          </Typography>
        </Box>

        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <Card sx={{ flex: 1, mr: 2 }}>
            <CardContent>
              <Typography variant="subtitle1" color="text.secondary">
                待機人数
              </Typography>
              <Typography variant="h4" color="primary">
                {status.waiting_count}名
              </Typography>
            </CardContent>
          </Card>
          <Card sx={{ flex: 1, mr: 2 }}>
            <CardContent>
              <Typography variant="subtitle1" color="text.secondary">
                あなたの番号
              </Typography>
              <Typography variant="h4">
                {userReservation?.reception_number
                  ? `No.${userReservation.reception_number}`
                  : "---"}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <br />

        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            mb: 2,
          }}
        >
          <Card sx={{ flex: 1, mr: 2 }}>
            <CardContent>
              <Typography variant="subtitle1" color="text.secondary">
                呼出中番号
              </Typography>
              <Typography variant="h4">
                {callingReservation?.reception_number
                  ? `No.${callingReservation.reception_number}`
                  : "---"}
              </Typography>
            </CardContent>
          </Card>
          <Card sx={{ flex: 1, mr: 2 }}>
            <CardContent>
              <Typography variant="subtitle1" color="text.secondary">
                最終受付番号
              </Typography>
              <Typography variant="h4">
                {latestReservation?.reception_number
                  ? `No.${latestReservation.reception_number}`
                  : "---"}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ReservationWaitingStatusCard;
