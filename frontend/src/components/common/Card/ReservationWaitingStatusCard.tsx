import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
} from "@mui/material";
import { useWaitingStatus } from "../../../hooks/useWaitingStatus";

interface ReservationWaitingStatusCardProps {
  companyId: string;
  branchId: string;
  reservation: any;
}

export const ReservationWaitingStatusCard: React.FC<
  ReservationWaitingStatusCardProps
> = ({ companyId, branchId, reservation }) => {
  const { status, isLoading, error } = useWaitingStatus(companyId, branchId);
  console.log("reservation", reservation);
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

        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 2 }}>
          <Box>
            <Typography variant="subtitle1" color="text.secondary">
              現在の呼び出し番号
            </Typography>
            <Typography variant="h4">
              {status.current_number ? `No.${status.current_number}` : "---"}
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle1" color="text.secondary">
              最終受付番号
            </Typography>
            <Typography variant="h4">
              {reservation?.reception_number
                ? `No.${reservation.reception_number}`
                : "---"}
            </Typography>
          </Box>
        </Box>

        <Box>
          <Typography variant="subtitle1" color="text.secondary">
            待機人数
          </Typography>
          <Typography variant="h4" color="primary">
            {status.waiting_count}名
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ReservationWaitingStatusCard;
