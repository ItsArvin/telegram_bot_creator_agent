"use client";

import { FormEvent, useEffect, useState } from "react";
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

type TelegramStatus = {
  connected: boolean;
  telegram_bot_id: number | null;
  username: string | null;
  first_name: string | null;
};

export default function BotWorkspacePage() {
  const params = useParams<{ botId: string }>();
  const router = useRouter();
  const [bot, setBot] = useState<Bot | null>(null);
  const [telegram, setTelegram] = useState<TelegramStatus | null>(null);
  const [token, setToken] = useState("");
  const [loadingTelegram, setLoadingTelegram] = useState(true);
  const [savingTelegram, setSavingTelegram] = useState(false);
  const [telegramError, setTelegramError] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const [botData, telegramData] = await Promise.all([
          api<Bot>("/bots/" + params.botId),
          api<TelegramStatus>("/bots/" + params.botId + "/telegram"),
        ]);
        if (!active) return;
        setBot(botData);
        setTelegram(telegramData);
      } catch (err) {
        if (!active) return;
        if (err instanceof Error && err.message === "Authentication required") {
          router.replace("/login");
          return;
        }
        setError(err instanceof Error ? err.message : "Could not load workspace");
      } finally {
        if (active) setLoadingTelegram(false);
      }
    }
    void load();
    return () => {
      active = false;
    };
  }, [params.botId, router]);

  async function connectTelegram(event: FormEvent) {
    event.preventDefault();
    setTelegramError("");
    const value = token.trim();
    if (!value) return;
    setSavingTelegram(true);
    try {
      const result = await api<TelegramStatus>("/bots/" + params.botId + "/telegram", {
        method: "POST",
        body: JSON.stringify({ token: value }),
      });
      setTelegram(result);
      setToken("");
    } catch (err) {
      setTelegramError(err instanceof Error ? err.message : "Could not connect Telegram");
    } finally {
      setSavingTelegram(false);
    }
  }

  async function disconnectTelegram() {
    setTelegramError("");
    setSavingTelegram(true);
    try {
      await api<void>("/bots/" + params.botId + "/telegram", { method: "DELETE" });
      setTelegram({ connected: false, telegram_bot_id: null, username: null, first_name: null });
    } catch (err) {
      setTelegramError(err instanceof Error ? err.message : "Could not disconnect Telegram");
    } finally {
      setSavingTelegram(false);
    }
  }

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
          <p className="muted">Natural-language bot building will be connected in the next phases.</p>
        </article>

        <article className="empty-card">
          <p className="eyebrow">TELEGRAM</p>
          <h2>Connection</h2>
          {loadingTelegram ? (
            <p className="muted">Checking connection…</p>
          ) : telegram?.connected ? (
            <>
              <p>
                Connected to <strong>@{telegram.username || telegram.first_name || "Telegram bot"}</strong>
              </p>
              <p className="muted">Bot ID: {telegram.telegram_bot_id}</p>
              {telegramError && <p className="error">{telegramError}</p>}
              <button className="secondary" onClick={disconnectTelegram} disabled={savingTelegram}>
                {savingTelegram ? "Disconnecting…" : "Disconnect"}
              </button>
            </>
          ) : (
            <form className="create-form" onSubmit={connectTelegram}>
              <label>
                Bot token
                <input
                  type="password"
                  value={token}
                  onChange={(event) => setToken(event.target.value)}
                  placeholder="123456789:AA..."
                  autoComplete="off"
                  required
                />
              </label>
              <p className="hint">Create a bot with @BotFather and paste its token here. The token is encrypted before it is stored.</p>
              {telegramError && <p className="error">{telegramError}</p>}
              <button disabled={savingTelegram || !token.trim()}>
                {savingTelegram ? "Connecting…" : "Connect Telegram"}
              </button>
            </form>
          )}
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
