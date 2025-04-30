import React from "react";
import { BottomNavigation, BottomNavigationAction } from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
// import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import HistoryIcon from "@mui/icons-material/History";
import HomeIcon from "@mui/icons-material/Home";
import { useNavigate } from "react-router-dom";

const CustomBottomNavigation = () => {
  const [value, setValue] = React.useState(0);
  const navigate = useNavigate();

  return (
    <BottomNavigation
      value={value}
      onChange={(event, newValue) => {
        setValue(newValue);
      }}
      sx={{ position: "fixed", bottom: 0, width: "100%" }}
    >
      <BottomNavigationAction
        label="ホーム"
        icon={<HomeIcon />}
        onClick={() => navigate("/dashboard")}
      />
      <BottomNavigationAction
        label="予約一覧"
        icon={<HistoryIcon />}
        onClick={() => navigate("/dashboard")}
      />
      <BottomNavigationAction
        label="プロフィール"
        icon={<AccountCircleIcon />}
        onClick={() => navigate("/profile")}
      />
    </BottomNavigation>
  );
};

export default CustomBottomNavigation;
