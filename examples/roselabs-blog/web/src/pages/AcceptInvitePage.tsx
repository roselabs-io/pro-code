import { Alert, Box, Button, Stack, TextField, Typography } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";
import { type FormEvent, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import { acceptInvite } from "../api";
import { useAuth } from "../auth";

export function AcceptInvitePage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { setSession } = useAuth();

  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const access = await acceptInvite(token, displayName, password);
      setSession(access);
      queryClient.invalidateQueries({ queryKey: ["me"] });
      navigate("/admin");
    } catch {
      setError("This invitation is invalid or has expired.");
    } finally {
      setBusy(false);
    }
  }

  if (!token) {
    return <Alert severity="error">This invitation link is missing its token.</Alert>;
  }

  return (
    <Box component="form" onSubmit={onSubmit} sx={{ maxWidth: 360, mx: "auto" }}>
      <Typography variant="h4" gutterBottom>
        Accept your invitation
      </Typography>
      <Stack spacing={2}>
        {error && <Alert severity="error">{error}</Alert>}
        <TextField
          label="Display name"
          value={displayName}
          onChange={(event) => setDisplayName(event.target.value)}
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
          Set password
        </Button>
      </Stack>
    </Box>
  );
}
