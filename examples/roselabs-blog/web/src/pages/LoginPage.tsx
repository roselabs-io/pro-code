import { Alert, Box, Button, Stack, TextField, Typography } from "@mui/material";
import { type FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await login(email, password);
      navigate("/admin");
    } catch {
      setError("Invalid email or password.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Box component="form" onSubmit={onSubmit} sx={{ maxWidth: 360, mx: "auto" }}>
      <Typography variant="h4" gutterBottom>
        Sign in
      </Typography>
      <Stack spacing={2}>
        {error && <Alert severity="error">{error}</Alert>}
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />
        <Button type="submit" variant="contained" disabled={busy}>
          Sign in
        </Button>
      </Stack>
    </Box>
  );
}
