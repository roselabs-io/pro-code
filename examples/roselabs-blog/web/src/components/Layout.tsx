import { AppBar, Box, Container, Toolbar, Typography } from "@mui/material";
import { Link, Outlet } from "react-router-dom";

export function Layout() {
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
      <AppBar
        position="static"
        color="transparent"
        elevation={0}
        sx={{ borderBottom: 1, borderColor: "divider" }}
      >
        <Toolbar>
          <Typography
            component={Link}
            to="/"
            variant="h6"
            sx={{ color: "text.primary", textDecoration: "none", flexGrow: 1 }}
          >
            roselabs · field notes
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ py: 5 }}>
        <Outlet />
      </Container>
    </Box>
  );
}
