import React from "react";
import { BottomNavigation, BottomNavigationAction, Paper } from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import BusinessIcon from "@mui/icons-material/Business";
import StoreIcon from "@mui/icons-material/Store";
import DashboardIcon from "@mui/icons-material/Dashboard";
import HomeIcon from "@mui/icons-material/Home";
import { useNavigate, useLocation } from "react-router-dom";

const CustomBottomNavigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // 現在のパスに基づいて選択されたタブを設定
  const getCurrentValue = () => {
    const path = location.pathname;
    if (path === "/") return 0;
    if (path.startsWith("/companies")) return 1;
    if (path.startsWith("/stores")) return 2;
    if (path.startsWith("/profile")) return 3;
    return 0;
  };

  return (
    <Paper
      sx={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
      }}
      elevation={3}
    >
      <BottomNavigation
        value={getCurrentValue()}
        onChange={(event, newValue) => {
          switch (newValue) {
            case 0:
              navigate("/dashboard");
              break;
            case 1:
              navigate("/companies");
              break;
            case 2:
              navigate("/stores");
              break;
            case 3:
              navigate("/profile");
              break;
          }
        }}
      >
        <BottomNavigationAction label="ホーム" icon={<DashboardIcon />} />
        <BottomNavigationAction label="企業" icon={<BusinessIcon />} />
        <BottomNavigationAction label="店舗" icon={<StoreIcon />} />
        <BottomNavigationAction
          label="プロフィール"
          icon={<AccountCircleIcon />}
        />
      </BottomNavigation>
    </Paper>
  );
};

export default CustomBottomNavigation;
