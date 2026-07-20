import { Alert, Box, CircularProgress, Typography } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";

import { fetchPublicPost } from "../api";
import { formatDate } from "../lib/format";

export function PostDetailPage() {
  const { slug = "" } = useParams();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["public-post", slug],
    queryFn: () => fetchPublicPost(slug),
    retry: false,
  });

  if (isLoading) {
    return <CircularProgress aria-label="Loading post" />;
  }
  if (isError || !data) {
    return <Alert severity="error">Post not found.</Alert>;
  }

  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        {data.title}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        {data.author_name}
        {data.published_at ? ` · ${formatDate(data.published_at)}` : ""}
      </Typography>
      {/* Decision 0001: the article's rich HTML renders in a sandboxed iframe (no
          allow-scripts) — full CSS/SVG isolation from the app, and no script runs. */}
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
    </Box>
  );
}
