import { expect, test } from "@playwright/test";

test("an author logs in, writes, publishes, and the post appears publicly", async ({
  page,
}) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("demo@roselabs.io");
  await page.getByLabel("Password").fill("demo-password-please-change");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/admin$/);

  await page.getByRole("link", { name: "New post" }).click();
  const title = `An e2e post ${Date.now()}`;
  await page.getByLabel("Title").fill(title);
  await page.getByLabel("Body (HTML)").fill("<h1>Written by the browser test</h1>");
  await page.getByRole("button", { name: "Publish" }).click();

  await expect(page).toHaveURL(/\/admin$/);
  await expect(page.getByText(title)).toBeVisible();

  await page.goto("/");
  await expect(page.getByText(title)).toBeVisible();
});

test("the login form rejects bad credentials without an oracle", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("nobody@roselabs.io");
  await page.getByLabel("Password").fill("wrong");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByText("Invalid email or password.")).toBeVisible();
});
