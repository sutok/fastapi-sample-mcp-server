import { Box, Container, AppBar, Toolbar, Typography } from "@mui/material";
import { styled } from "@mui/material/styles";

interface LayoutProps {
  children: React.ReactNode;
}

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  color: theme.palette.text.primary,
  boxShadow: "none",
  borderBottom: `1px solid ${theme.palette.divider}`,
}));

const Main = styled("main")(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  backgroundColor: theme.palette.background.default,
  minHeight: "100vh",
}));

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: "flex", flexDirection: "column" }}>
      <StyledAppBar position="static">
        <Toolbar>
          <Typography variant="h6">予約システム</Typography>
        </Toolbar>
      </StyledAppBar>
      <Main>
        <Container maxWidth="lg">{children}</Container>
      </Main>
    </Box>
  );
};
