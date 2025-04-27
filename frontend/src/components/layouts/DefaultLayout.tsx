import * as React from "react";
import { signOut } from "firebase/auth";
import { auth } from "../../firebase";
import { useNavigate } from "react-router-dom";
import {
  Box,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  ListItemButton,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LogoutIcon from "@mui/icons-material/Logout";
import Dashboard from "../../pages/Dashboard";

const drawerWidth = 240;

type Props = {
  children: React.ReactNode;
};

const menuItems = [
  { text: "プロフィール", icon: <AccountCircleIcon />, path: "/profile" },
];

const DefaultLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    console.log("logout click");
    try {
      await signOut(auth);
      navigate("/login");
    } catch (e) {
      alert("ログアウトに失敗しました");
    }
  };

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            サービス名ダッシュボード
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto" }}>
          <List>
            <ListItem disablePadding>
              <ListItemButton component="a" href={"/dashboard"}>
                <ListItemIcon>
                  <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary={"ダッシュボード"} />
              </ListItemButton>
            </ListItem>
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton component="a" href={item.path}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
          <Divider />
          <ListItem disablePadding>
            <ListItemButton component="a" href="/logout">
              <ListItemIcon>
                <LogoutIcon />
              </ListItemIcon>
              <ListItemText primary={"ログアウト"} />
            </ListItemButton>
          </ListItem>
        </Box>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, bgcolor: "background.default", p: 3 }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default DefaultLayout;
