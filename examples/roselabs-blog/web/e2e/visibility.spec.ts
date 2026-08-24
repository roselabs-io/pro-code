import { expect, test } from "@playwright/test";

// The browser grader: it drives the running app and asserts on the rendered DOM —
// the load-bearing visual invariant is that a draft never appears for an anon visitor.

test("home lists published posts but not the draft", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Welcome to the roselabs blog")).toBeVisible();
  await expect(page.getByText("The iframe test")).toBeVisible();
  await expect(page.getByText("A secret draft")).toHaveCount(0);
});

test("a published article renders inside a sandboxed iframe", async ({ page }) => {
  await page.goto("/posts/the-iframe-test");
  const frame = page.getByTestId("article-frame");
  await expect(frame).toBeVisible();
  await expect(frame).toHaveAttribute("sandbox", "");
});

test("a draft slug shows not-found, never its content", async ({ page }) => {
  await page.goto("/posts/a-secret-draft");
  await expect(page.getByText("Post not found")).toBeVisible();
  await expect(page.getByText("must never appear publicly")).toHaveCount(0);
});
