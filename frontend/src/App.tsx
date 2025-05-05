import React from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
// import Button from "@mui/material/Button";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginLayout from "./components/layouts/LoginLayout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
// import ProfileEdit from "./pages/ProfileEdit";
import Logout from "./pages/Logout";
import SignUp from "./pages/SignUp";
import Home from "./pages/Home";
import CustomBottomNavigation from "./components/common/BottomNavigation";
import Box from "@mui/material/Box";
import Companies from "./pages/Companies";
import Branches from "./pages/Branches";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Reservations from "./pages/Reservations";

const theme = createTheme({
  palette: {
    mode: "light", // 'dark'にするとダークモード
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#dc004e",
    },
  },
});

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <Box sx={{ pb: 7 }}>
            <Routes>
              <Route element={<LoginLayout />}>
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/logout" element={<Logout />} />
              </Route>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/" element={<Home />} />
              <Route path="/companies" element={<Companies />} />
              <Route
                path="/company/:company_id/branches"
                element={<Branches />}
              />
              <Route
                path="/company/:company_id/branches/:branch_id/reservations"
                element={<Reservations />}
              />
            </Routes>
            <CustomBottomNavigation />
          </Box>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;
