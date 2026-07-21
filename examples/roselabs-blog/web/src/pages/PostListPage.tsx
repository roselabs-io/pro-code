import {
  Alert,
  Box,
  Card,
  CardActionArea,
  CardContent,
  Chip,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { Link, useSearchParams } from "react-router-dom";

import { fetchPublicPosts } from "../api";
import { formatDate } from "../lib/format";

export function PostListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const tag = searchParams.get("tag") ?? undefined;
  const { data, isLoading, isError } = useQuery({
    queryKey: ["public-posts", tag ?? null],
    queryFn: () => fetchPublicPosts(tag),
  });

  if (isLoading) {
    return <CircularProgress aria-label="Loading posts" />;
  }
  if (isError) {
    return <Alert severity="error">Couldn&apos;t load posts. Please retry.</Alert>;
  }

  const items = data?.items ?? [];

  return (
    <Box>
      {tag && (
        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 2 }}>
          <Typography color="text.secondary">Tagged</Typography>
          <Chip label={tag} onDelete={() => setSearchParams({})} />
        </Stack>
      )}

      {items.length === 0 ? (
        <Typography color="text.secondary">No posts yet.</Typography>
      ) : (
        <Stack spacing={2} data-testid="post-list">
          {items.map((post) => (
            <Card key={post.slug} variant="outlined" sx={{ bgcolor: "background.paper" }}>
              <CardActionArea component={Link} to={`/posts/${post.slug}`}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {post.title}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {post.author_name}
                    {post.published_at ? ` · ${formatDate(post.published_at)}` : ""}
                  </Typography>
                  <Typography sx={{ mt: 1 }} color="text.secondary">
                    {post.excerpt}
                  </Typography>
                </CardContent>
              </CardActionArea>
              {post.tags.length > 0 && (
                <Stack
                  direction="row"
                  sx={{ px: 2, pb: 2, flexWrap: "wrap", gap: 1 }}
                >
                  {post.tags.map((name) => (
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
            </Card>
          ))}
        </Stack>
      )}
    </Box>
  );
}
