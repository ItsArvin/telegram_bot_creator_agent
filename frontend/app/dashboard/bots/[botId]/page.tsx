"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { api } from "../../../lib/api";

type Bot = {
  id: string;
  name: string;
  description: string | null;
  status: string;
  current_version_id: string | null;
  created_at: string;
  updated_at: string;
};

export default function BotWorkspacePage() {
  const params = useParams<{ botId: string }>();
  const router = useRouter();
  const [bot, setBot] = useState<Bot | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    api<Bot>("/bots/" + params.botId)
      .then((data) => {
        if (active) setBot(data);
      })
      .catch((err) => {
        if (!active) return;
        if (err instanceof Error && err.message === "Authentication required") {
          router.replace("/login");
          return;
        }
        setError(err instanceof Error ? err.message : "Could not load bot");
      });
    return () => {
      active = false;
    };
  }, [params.botId, router]);

  if (error) {
    return (
      <main className="center-page">
        <div className="empty-card">
          <h2>Workspace unavailable</h2>
          <p className="muted">{error}</p>
          <Link className="button secondary" href="/dashboard">Back to dashboard</Link>
        </div>
      </main>
    );
  }

  if (!bot) {
    return <main className="center-page"><p className="muted">Loading workspace…</p></main>;
  }

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <div>
          <Link className="muted" href="/dashboard">← My Bots</Link>
          <p className="eyebrow">BOT WORKSPACE</p>
          <h1>{bot.name}</h1>
          <p className="muted">{bot.description || "No description yet."}</p>
        </div>
        <span className="badge">{bot.status}</span>
      </header>

      <section className="workspace-grid">
        <article className="empty-card">
          <p className="eyebrow">CHAT</p>
          <h2>AI workspace</h2>
          <p className="muted">Natural-language bot building will be connected in Phase 4/5.</p>
        </article>
        <article className="empty-card">
          <p className="eyebrow">TELEGRAM</p>
          <h2>Connection</h2>
          <p className="muted">Telegram credentials will be connected in Phase 3.</p>
        </article>
        <article className="empty-card">
          <p className="eyebrow">VERSIONS</p>
          <h2>Current version</h2>
          <p className="muted">{bot.current_version_id ? "A current version is selected." : "No version created yet."}</p>
        </article>
        <article className="empty-card">
          <p className="eyebrow">WORKSPACE</p>
          <h2>Persistent state</h2>
          <p className="muted">Created {new Date(bot.created_at).toLocaleString()} · Updated {new Date(bot.updated_at).toLocaleString()}</p>
        </article>
      </section>
    </main>
  );
}
