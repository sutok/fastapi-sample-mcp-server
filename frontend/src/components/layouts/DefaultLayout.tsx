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
  IconButton,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LogoutIcon from "@mui/icons-material/Logout";
import MenuIcon from "@mui/icons-material/Menu";
import Dashboard from "../../pages/Dashboard";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";

const drawerWidth = 240;

type Props = {
  children: React.ReactNode;
};

const menuItems = [
  { text: "ダッシュボード", icon: <DashboardIcon />, path: "/dashboard" },
  { text: "プロフィール", icon: <AccountCircleIcon />, path: "/profile" },
  { text: "ログアウト", icon: <LogoutIcon />, logout: true },
];

const DefaultLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = async () => {
    console.log("logout click");
    try {
      await signOut(auth);
      navigate("/login");
    } catch (e) {
      alert("ログアウトに失敗しました");
    }
  };

  const drawer = (
    <Box sx={{ overflow: "auto" }}>
      <List>
        {menuItems.map((item) => (
          <React.Fragment key={item.text}>
            {item.text === "ログアウト" && <Divider />}
            <ListItem disablePadding>
              {item.logout ? (
                <ListItemButton onClick={handleLogout}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              ) : (
                <ListItemButton component="a" href={item.path}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              )}
            </ListItem>
          </React.Fragment>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', flexDirection: 'column' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: "none" } }}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" noWrap component="div">
            サービス名ダッシュボード
          </Typography>
        </Toolbar>
      </AppBar>

      {/* モバイル用Drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // モバイルパフォーマンス向上
        }}
        sx={{
          display: { xs: "block", sm: "none" },
          "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
        }}
      >
        <Toolbar />
        {drawer}
      </Drawer>

      {/* PC用Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", sm: "block" },
          "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
        }}
        open
      >
        <Toolbar />
        {drawer}
      </Drawer>

      <Box sx={{ flexGrow: 1, display: 'flex' }}>
        <Box
          component="main"
          sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
        >
          <Toolbar />
          {children}
        </Box>
      </Box>

      {/* フッター（画面下部に固定） */}
      <Box
        component="footer"
        sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          width: '100%',
          bgcolor: 'grey.200',
          py: 2,
          textAlign: 'center',
          zIndex: (theme) => theme.zIndex.drawer + 1,
        }}
      >
        <Typography variant="body2" color="text.secondary">
          © {new Date().getFullYear()} サービス名. All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
};

export default DefaultLayout;
