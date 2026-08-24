import { expect, type Page, test } from "@playwright/test";

async function login(page: Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("demo@roselabs.io");
  await page.getByLabel("Password").fill("demo-password-please-change");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/admin$/);
}

test("a comment is held for moderation, then appears once approved", async ({ page }) => {
  const body = `A comment from e2e ${Date.now()}`;

  await page.goto("/posts/welcome");
  await page.getByLabel("Name").fill("Visitor");
  await page.getByLabel("Email").fill("visitor@example.com");
  await page.getByLabel("Comment").fill(body);
  await page.getByRole("button", { name: "Submit" }).click();
  await expect(page.getByText("pending review")).toBeVisible();

  // Not shown before moderation.
  await page.reload();
  await expect(page.getByText(body)).toHaveCount(0);

  // The author approves it.
  await login(page);
  await page.goto("/admin/moderation");
  const card = page
    .getByTestId("pending-comments")
    .locator("> *")
    .filter({ hasText: body });
  await card.getByRole("button", { name: "Approve" }).click();

  // Now visible publicly.
  await page.goto("/posts/welcome");
  await expect(page.getByText(body)).toBeVisible();
});
