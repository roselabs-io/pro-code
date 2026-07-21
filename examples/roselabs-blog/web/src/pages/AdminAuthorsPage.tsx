import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { type FormEvent, useState } from "react";

import { inviteAuthor, listAuthors } from "../api";

export function AdminAuthorsPage() {
  const queryClient = useQueryClient();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["authors"],
    queryFn: listAuthors,
  });
  const [email, setEmail] = useState("");
  const invite = useMutation({
    mutationFn: () => inviteAuthor(email),
    onSuccess: () => {
      setEmail("");
      queryClient.invalidateQueries({ queryKey: ["authors"] });
    },
  });

  if (isLoading) {
    return <CircularProgress aria-label="Loading authors" />;
  }
  if (isError) {
    return <Alert severity="error">Admins only.</Alert>;
  }

  const authors = data ?? [];

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    invite.mutate();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Authors
      </Typography>
      <Box component="form" onSubmit={onSubmit} sx={{ mb: 3 }}>
        {invite.isSuccess && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Invitation sent (logged in dev).
          </Alert>
        )}
        <Stack direction="row" spacing={2}>
          <TextField
            label="Invite by email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            sx={{ flexGrow: 1 }}
          />
          <Button type="submit" variant="contained" disabled={invite.isPending}>
            Send invite
          </Button>
        </Stack>
      </Box>
      <Stack spacing={1}>
        {authors.map((author) => (
          <Stack
            key={author.id}
            direction="row"
            spacing={2}
            alignItems="center"
            sx={{ p: 1.5, border: 1, borderColor: "divider", borderRadius: 1 }}
          >
            <Typography sx={{ flexGrow: 1 }}>
              {author.display_name}{" "}
              <Typography component="span" color="text.secondary">
                &lt;{author.email}&gt;
              </Typography>
            </Typography>
            <Chip
              size="small"
              label={author.role}
              color={author.role === "admin" ? "success" : "default"}
            />
          </Stack>
        ))}
      </Stack>
    </Box>
  );
}
