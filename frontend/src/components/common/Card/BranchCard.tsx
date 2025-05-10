import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { Branch } from "../../../types"; // 型定義ファイルのパスに合わせて修正
import { useNavigate, useParams } from "react-router-dom";

type BranchCardProps = {
  branch: Branch;
};

const BranchCard: React.FC<BranchCardProps> = ({ branch }) => {
  const navigate = useNavigate();
  // パラメータ取得
  const { company_id } = useParams<{ company_id: string }>();

  return (
    <Box sx={{ minWidth: 275 }}>
      <Card variant="outlined">
        <React.Fragment>
          <CardActionArea
            onClick={() =>
              navigate(
                `/company/${company_id}/branches/${branch.id}/reservations`
              )
            }
          >
            <CardContent>
              <Typography variant="h5" component="div">
                {branch.branch_name}
              </Typography>
              <Typography sx={{ color: "text.secondary", mb: 0.5 }}>
                TEL: {branch.phone}
              </Typography>
              <Typography variant="body2">
                営業時間: {branch.business_hours}
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  textAlign: "right",
                  color: "primary.main",
                  textDecoration: "underline",
                  cursor: "pointer",
                }}
              >
                予約へ
              </Typography>
            </CardContent>
          </CardActionArea>
          <CardActions>
            <Button size="small">店舗詳細</Button>
          </CardActions>
        </React.Fragment>
      </Card>
    </Box>
    // <h3>{branch.branch_name}</h3>
  );
};

export default BranchCard;
