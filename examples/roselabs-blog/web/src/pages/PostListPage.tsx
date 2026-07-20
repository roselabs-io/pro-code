import {
  Alert,
  Card,
  CardActionArea,
  CardContent,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { fetchPublicPosts } from "../api";
import { formatDate } from "../lib/format";

export function PostListPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["public-posts"],
    queryFn: fetchPublicPosts,
  });

  if (isLoading) {
    return <CircularProgress aria-label="Loading posts" />;
  }
  if (isError) {
    return <Alert severity="error">Couldn&apos;t load posts. Please retry.</Alert>;
  }
  if (!data || data.items.length === 0) {
    return <Typography color="text.secondary">No posts yet.</Typography>;
  }

  return (
    <Stack spacing={2} data-testid="post-list">
      {data.items.map((post) => (
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
        </Card>
      ))}
    </Stack>
  );
}
