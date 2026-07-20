import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { listMyPosts, publishPost, unpublishPost } from "../api";
import { formatDate } from "../lib/format";

export function DashboardPage() {
  const queryClient = useQueryClient();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["my-posts"],
    queryFn: listMyPosts,
  });
  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: ["my-posts"] });
  const publish = useMutation({ mutationFn: publishPost, onSuccess: invalidate });
  const unpublish = useMutation({ mutationFn: unpublishPost, onSuccess: invalidate });

  if (isLoading) {
    return <CircularProgress aria-label="Loading your posts" />;
  }
  if (isError) {
    return <Alert severity="error">Couldn&apos;t load your posts.</Alert>;
  }

  const posts = data ?? [];

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 3 }}
      >
        <Typography variant="h4">My posts</Typography>
        <Button component={Link} to="/admin/new" variant="contained">
          New post
        </Button>
      </Stack>

      {posts.length === 0 ? (
        <Typography color="text.secondary">No posts yet — write one.</Typography>
      ) : (
        <Stack spacing={1} data-testid="dashboard-posts">
          {posts.map((post) => (
            <Stack
              key={post.id}
              direction="row"
              spacing={2}
              alignItems="center"
              sx={{ p: 1.5, border: 1, borderColor: "divider", borderRadius: 1 }}
            >
              <Chip
                size="small"
                label={post.status}
                color={post.status === "published" ? "success" : "default"}
              />
              <Typography sx={{ flexGrow: 1 }}>{post.title}</Typography>
              <Typography variant="caption" color="text.secondary">
                {formatDate(post.published_at)}
              </Typography>
              <Button size="small" component={Link} to={`/admin/posts/${post.id}`}>
                Edit
              </Button>
              {post.status === "published" ? (
                <Button size="small" onClick={() => unpublish.mutate(post.id)}>
                  Unpublish
                </Button>
              ) : (
                <Button size="small" onClick={() => publish.mutate(post.id)}>
                  Publish
                </Button>
              )}
            </Stack>
          ))}
        </Stack>
      )}
    </Box>
  );
}
