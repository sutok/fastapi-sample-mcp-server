import React from "react";
import { Card, CardContent, Typography } from "@mui/material";
import { Reservation, Branch } from "../../../types";

interface ReservationCardProps {
  reservation: Reservation;
  branch?: Branch;
}

const ReservationCard: React.FC<ReservationCardProps> = ({
  reservation,
  branch,
}) => {
  return (
    <Card variant="outlined" sx={{ mb: 1 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          予約番号: {reservation.id}
        </Typography>
        <Typography sx={{ color: "text.secondary", mb: 0.5 }}>
          店舗: {branch?.branch_name}
        </Typography>
        <Typography sx={{ color: "text.secondary", mb: 0.5 }}>
          TEL: {branch?.phone}
        </Typography>
        <Typography variant="body2">
          営業時間: {branch?.business_hours}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ReservationCard;
