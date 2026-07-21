import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useMutation, useQuery } from "@tanstack/react-query";
import { type FormEvent, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { fetchPublicPost, submitComment } from "../api";
import { formatDate } from "../lib/format";

export function PostDetailPage() {
  const { slug = "" } = useParams();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["public-post", slug],
    queryFn: () => fetchPublicPost(slug),
    retry: false,
  });

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [body, setBody] = useState("");
  const submit = useMutation({
    mutationFn: () =>
      submitComment(slug, { author_name: name, author_email: email, body }),
    onSuccess: () => {
      setName("");
      setEmail("");
      setBody("");
    },
  });

  if (isLoading) {
    return <CircularProgress aria-label="Loading post" />;
  }
  if (isError || !data) {
    return <Alert severity="error">Post not found.</Alert>;
  }

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    submit.mutate();
  };

  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        {data.title}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        {data.author_name}
        {data.published_at ? ` · ${formatDate(data.published_at)}` : ""}
      </Typography>
      {data.tags.length > 0 && (
        <Stack direction="row" sx={{ mt: 1, flexWrap: "wrap", gap: 1 }}>
          {data.tags.map((name) => (
            <Chip
              key={name}
              label={name}
              size="small"
              clickable
              component={Link}
              to={`/?tag=${encodeURIComponent(name)}`}
            />
          ))}
        </Stack>
      )}
      {/* Decision 0001: the article renders in a sandboxed iframe (no allow-scripts). */}
      <Box
        component="iframe"
        title={data.title}
        srcDoc={data.content_html}
        sandbox=""
        data-testid="article-frame"
        sx={{
          width: "100%",
          minHeight: "72vh",
          border: 0,
          mt: 3,
          borderRadius: 1,
          bgcolor: "common.white",
        }}
      />

      <Divider sx={{ my: 4 }} />
      <Typography variant="h5" gutterBottom>
        Comments ({data.comments.length})
      </Typography>
      <Stack spacing={2} sx={{ mb: 4 }} data-testid="comments">
        {data.comments.length === 0 ? (
          <Typography color="text.secondary">No comments yet.</Typography>
        ) : (
          data.comments.map((comment, index) => (
            <Box
              key={index}
              sx={{ p: 2, border: 1, borderColor: "divider", borderRadius: 1 }}
            >
              <Typography variant="caption" color="text.secondary">
                {comment.author_name} · {formatDate(comment.created_at)}
              </Typography>
              {/* Plain text — React escapes it, so injected markup can't execute. */}
              <Typography>{comment.body}</Typography>
            </Box>
          ))
        )}
      </Stack>

      <Box component="form" onSubmit={onSubmit}>
        <Typography variant="h6" gutterBottom>
          Leave a comment
        </Typography>
        {submit.isSuccess && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Thanks — your comment is pending review.
          </Alert>
        )}
        <Stack spacing={2}>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <TextField
              label="Name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
              fullWidth
            />
            <TextField
              label="Email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              fullWidth
            />
          </Stack>
          <TextField
            label="Comment"
            value={body}
            onChange={(event) => setBody(event.target.value)}
            required
            multiline
            minRows={3}
          />
          <Box>
            <Button type="submit" variant="contained" disabled={submit.isPending}>
              Submit
            </Button>
          </Box>
        </Stack>
      </Box>
    </Box>
  );
}
