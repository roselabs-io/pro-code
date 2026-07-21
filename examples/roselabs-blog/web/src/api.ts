import axios from "axios";

export const api = axios.create({ baseURL: "/api" });

const TOKEN_KEY = "blog_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string | null): void {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ---- public ----

export interface PostSummary {
  slug: string;
  title: string;
  excerpt: string;
  published_at: string | null;
  author_name: string;
}

export interface PublicComment {
  author_name: string;
  body: string;
  created_at: string;
}

export interface PostDetail extends PostSummary {
  content_html: string;
  comments: PublicComment[];
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

// ---- auth ----

export interface Me {
  id: string;
  email: string;
  display_name: string;
  role: string;
}

export async function login(email: string, password: string): Promise<string> {
  const { data } = await api.post<{ access_token: string }>("/auth/login", {
    email,
    password,
  });
  return data.access_token;
}

export async function fetchMe(): Promise<Me> {
  const { data } = await api.get<Me>("/auth/me");
  return data;
}

// ---- authored posts ----

export type PostStatus = "draft" | "published";

export interface AuthoredPost {
  id: string;
  author_id: string;
  title: string;
  slug: string;
  content_html: string;
  excerpt: string;
  status: PostStatus;
  published_at: string | null;
  created_at: string;
}

export interface PostInput {
  title: string;
  content_html: string;
  excerpt?: string;
}

export async function listMyPosts(): Promise<AuthoredPost[]> {
  const { data } = await api.get<AuthoredPost[]>("/posts/mine");
  return data;
}

export async function getMyPost(id: string): Promise<AuthoredPost> {
  const { data } = await api.get<AuthoredPost>(`/posts/${id}`);
  return data;
}

export async function createPost(input: PostInput): Promise<AuthoredPost> {
  const { data } = await api.post<AuthoredPost>("/posts", input);
  return data;
}

export async function updatePost(
  id: string,
  input: Partial<PostInput>,
): Promise<AuthoredPost> {
  const { data } = await api.patch<AuthoredPost>(`/posts/${id}`, input);
  return data;
}

export async function publishPost(id: string): Promise<AuthoredPost> {
  const { data } = await api.post<AuthoredPost>(`/posts/${id}/publish`);
  return data;
}

export async function unpublishPost(id: string): Promise<AuthoredPost> {
  const { data } = await api.post<AuthoredPost>(`/posts/${id}/unpublish`);
  return data;
}

// ---- comments ----

export interface CommentInput {
  author_name: string;
  author_email: string;
  body: string;
}

export interface ModerationComment {
  id: string;
  post_slug: string;
  post_title: string;
  author_name: string;
  author_email: string;
  body: string;
  status: string;
  created_at: string;
}

export async function submitComment(slug: string, input: CommentInput): Promise<void> {
  await api.post(`/public/posts/${slug}/comments`, input);
}

export async function listPendingComments(): Promise<ModerationComment[]> {
  const { data } = await api.get<ModerationComment[]>("/comments/pending");
  return data;
}

export async function approveComment(id: string): Promise<void> {
  await api.post(`/comments/${id}/approve`);
}

export async function hideComment(id: string): Promise<void> {
  await api.post(`/comments/${id}/hide`);
}
