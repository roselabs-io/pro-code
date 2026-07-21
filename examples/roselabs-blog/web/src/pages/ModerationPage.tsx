import { Alert, Box, Button, CircularProgress, Stack, Typography } from "@mui/material";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { approveComment, hideComment, listPendingComments } from "../api";

export function ModerationPage() {
  const queryClient = useQueryClient();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["pending-comments"],
    queryFn: listPendingComments,
  });
  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: ["pending-comments"] });
  const approve = useMutation({ mutationFn: approveComment, onSuccess: invalidate });
  const hide = useMutation({ mutationFn: hideComment, onSuccess: invalidate });

  if (isLoading) {
    return <CircularProgress aria-label="Loading pending comments" />;
  }
  if (isError) {
    return <Alert severity="error">Couldn&apos;t load pending comments.</Alert>;
  }

  const comments = data ?? [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Pending comments
      </Typography>
      {comments.length === 0 ? (
        <Typography color="text.secondary">Nothing to moderate.</Typography>
      ) : (
        <Stack spacing={2} data-testid="pending-comments">
          {comments.map((comment) => (
            <Box
              key={comment.id}
              sx={{ p: 2, border: 1, borderColor: "divider", borderRadius: 1 }}
            >
              <Typography variant="caption" color="text.secondary">
                on &ldquo;{comment.post_title}&rdquo; · {comment.author_name}
              </Typography>
              <Typography sx={{ my: 1 }}>{comment.body}</Typography>
              <Stack direction="row" spacing={1}>
                <Button
                  size="small"
                  variant="contained"
                  onClick={() => approve.mutate(comment.id)}
                >
                  Approve
                </Button>
                <Button size="small" onClick={() => hide.mutate(comment.id)}>
                  Hide
                </Button>
              </Stack>
            </Box>
          ))}
        </Stack>
      )}
    </Box>
  );
}
