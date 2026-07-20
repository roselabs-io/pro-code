import axios from "axios";

export const api = axios.create({ baseURL: "/api" });

export interface PostSummary {
  slug: string;
  title: string;
  excerpt: string;
  published_at: string | null;
  author_name: string;
}

export interface PostDetail extends PostSummary {
  content_html: string;
}

export interface PublicList {
  items: PostSummary[];
  next_cursor: string | null;
}

export async function fetchPublicPosts(): Promise<PublicList> {
  const { data } = await api.get<PublicList>("/public/posts");
  return data;
}

export async function fetchPublicPost(slug: string): Promise<PostDetail> {
  const { data } = await api.get<PostDetail>(`/public/posts/${slug}`);
  return data;
}
