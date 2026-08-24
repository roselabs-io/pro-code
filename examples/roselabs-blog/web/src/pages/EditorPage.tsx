import { Alert, Box, Button, Stack, TextField, Typography } from "@mui/material";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { createPost, getMyPost, publishPost, updatePost } from "../api";

export function EditorPage() {
  const { id } = useParams();
  const editing = Boolean(id);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [title, setTitle] = useState("");
  const [excerpt, setExcerpt] = useState("");
  const [contentHtml, setContentHtml] = useState("");
  const [tagsText, setTagsText] = useState("");

  const existing = useQuery({
    queryKey: ["my-post", id],
    queryFn: () => getMyPost(id as string),
    enabled: editing,
    retry: false,
  });

  useEffect(() => {
    if (existing.data) {
      setTitle(existing.data.title);
      setExcerpt(existing.data.excerpt);
      setContentHtml(existing.data.content_html);
      setTagsText(existing.data.tags.join(", "));
    }
  }, [existing.data]);

  const save = useMutation({
    mutationFn: async (publish: boolean): Promise<void> => {
      const input = {
        title,
        content_html: contentHtml,
        excerpt,
        tags: tagsText
          .split(",")
          .map((tag) => tag.trim())
          .filter(Boolean),
      };
      const postId = editing
        ? ((await updatePost(id as string, input)) && (id as string))
        : (await createPost(input)).id;
      if (publish) {
        await publishPost(postId);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["my-posts"] });
      navigate("/admin");
    },
  });

  if (editing && existing.isError) {
    return <Alert severity="error">Post not found.</Alert>;
  }

  const canPublish = title.trim().length > 0 && contentHtml.trim().length > 0;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {editing ? "Edit post" : "New post"}
      </Typography>
      <Stack spacing={2}>
        <TextField
          label="Title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
        />
        <TextField
          label="Excerpt"
          value={excerpt}
          onChange={(event) => setExcerpt(event.target.value)}
          multiline
          minRows={2}
        />
        <TextField
          label="Tags (comma-separated)"
          value={tagsText}
          onChange={(event) => setTagsText(event.target.value)}
          placeholder="ai, control"
        />
        <TextField
          label="Body (HTML)"
          value={contentHtml}
          onChange={(event) => setContentHtml(event.target.value)}
          multiline
          minRows={10}
          slotProps={{ htmlInput: { style: { fontFamily: "monospace" } } }}
        />
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            disabled={save.isPending || !canPublish}
            onClick={() => save.mutate(false)}
          >
            Save draft
          </Button>
          <Button
            variant="contained"
            disabled={save.isPending || !canPublish}
            onClick={() => save.mutate(true)}
          >
            Publish
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
}
