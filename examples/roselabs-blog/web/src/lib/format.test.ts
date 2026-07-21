import { describe, expect, it } from "vitest";

import { formatDate } from "./format";

describe("formatDate", () => {
  it("returns an empty string for null", () => {
    expect(formatDate(null)).toBe("");
  });

  it("formats an ISO timestamp to a non-empty string", () => {
    expect(formatDate("2026-07-20T00:00:00Z")).not.toBe("");
  });
});
