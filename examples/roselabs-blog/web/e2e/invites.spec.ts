import { expect, test } from "@playwright/test";

test("an admin can reach Authors and send an invite", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("demo@roselabs.io");
  await page.getByLabel("Password").fill("demo-password-please-change");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/admin$/);

  await page.getByRole("link", { name: "Authors" }).click();
  await expect(page).toHaveURL(/\/admin\/authors$/);

  await page.getByLabel("Invite by email").fill(`invitee-${Date.now()}@example.com`);
  await page.getByRole("button", { name: "Send invite" }).click();
  await expect(page.getByText("Invitation sent")).toBeVisible();
});
