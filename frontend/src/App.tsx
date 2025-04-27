import React from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Button from "@mui/material/Button";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginLayout from "./components/layouts/LoginLayout";
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
    <BrowserRouter>
      <Routes>
        <Route element={<LoginLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/logout" element={<Logout />} />
        </Route>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
