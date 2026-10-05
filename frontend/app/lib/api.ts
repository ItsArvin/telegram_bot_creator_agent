const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\\/$/, "");

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  if (!API_URL) {
    throw new Error("NEXT_PUBLIC_API_URL is not configured");
  }

  const r = await fetch(`${API_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(init.headers ?? {}) },
  });

  if (!r.ok) {
    const body = await r.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed (${r.status})`);
  }
  if (r.status === 204) return undefined as T;
  return r.json();
}
export type User={id:string;email:string;created_at:string};
