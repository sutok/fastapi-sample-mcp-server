import React from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Button from "@mui/material/Button";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ProfileEdit from "./pages/ProfileEdit";
import Logout from "./pages/Logout";
import SignUp from "./pages/SignUp";

const theme = createTheme({
  palette: {
    mode: "light", // 'dark'にするとダークモード
    primary: {
      main: "#1976d2",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile/edit" element={<ProfileEdit />} />
          <Route path="/logout" element={<Logout />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
