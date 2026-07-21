import { AppBar, Box, Button, Container, Stack, Toolbar, Typography } from "@mui/material";
import { Link, Outlet } from "react-router-dom";

import { useAuth } from "../auth";

export function Layout() {
  const { isAuthed, logout } = useAuth();
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
          <Stack direction="row" spacing={1}>
            {isAuthed ? (
              <>
                <Button component={Link} to="/admin" color="inherit">
                  Dashboard
                </Button>
                <Button component={Link} to="/admin/moderation" color="inherit">
                  Moderation
                </Button>
                <Button onClick={logout} color="inherit">
                  Sign out
                </Button>
              </>
            ) : (
              <Button component={Link} to="/login" color="inherit">
                Sign in
              </Button>
            )}
          </Stack>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ py: 5 }}>
        <Outlet />
      </Container>
    </Box>
  );
}
