"use client";

import { useEffect, useRef, useState } from "react";
import fallbackData from "../public/telemetry_fallback_v2.4.json";
import { API_BASE_URL } from "../lib/api";

type MetricsSummary = {
  total_traces_evaluated: number;
  zero_day_block_rate_pct: number;
  false_positive_rate_pct: number;
  safe_auto_grant_accuracy_pct: number;
  p95_latency_ms: number;
  cost_per_1k_actions_usd: number;
  tier_distribution: { tier_0: number; tier_1: number; tier_2: number };
  capability: string;
};

type PolicyEvent = {
  id: string;
  label: string;
  decision: string;
  tier: string;
  latency: number;
  source: "live" | "replay";
};

const initialSummary = fallbackData.summary as MetricsSummary;
const replayEvents: PolicyEvent[] = fallbackData.events.map((event) => ({
  id: String(event.id),
  label: String(event.payload.trace_id ?? "Recorded policy event"),
  decision: String(event.payload.decision ?? "ALLOWED"),
  tier: String(event.payload.tier_resolved ?? "TIER_0"),
  latency: Number(event.payload.latency_ms ?? 0),
  source: "replay",
}));

function formatNumber(value: number, digits = 0): string {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: digits }).format(value);
}

export default function Home() {
  const [summary, setSummary] = useState(initialSummary);
  const [events, setEvents] = useState<PolicyEvent[]>(replayEvents.slice(-6).reverse());
  const [connection, setConnection] = useState<"connecting" | "live" | "fallback">("connecting");
  const replayIndex = useRef(0);

  useEffect(() => {
    let active = true;
    let streamConnected = false;
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 3000);
    const stream = new EventSource(`${API_BASE_URL}/v1/policy/stream`);

    const onPolicyEvent = (event: Event) => {
      try {
        const payload = JSON.parse((event as MessageEvent<string>).data) as Record<string, unknown>;
        const policyEvent: PolicyEvent = {
          id: String(payload.event_id ?? `${Date.now()}`),
          label: String(payload.command ?? payload.status ?? "Policy update"),
          decision: String(payload.decision ?? payload.status ?? "UPDATE"),
          tier: String(payload.tier_resolved ?? "TIER_2"),
          latency: Number(payload.latency_ms ?? 0),
          source: "live",
        };
        if (active) {
          setEvents((current) => [policyEvent, ...current].slice(0, 8));
        }
      } catch {
        if (active) setConnection("fallback");
        stream.close();
      }
    };

    stream.onopen = () => {
      streamConnected = true;
      if (active) setConnection("live");
    };
    stream.onerror = () => {
      stream.close();
      if (active) setConnection("fallback");
    };
    for (const eventName of ["evaluate", "tier2_state", "rule_promoted", "dropped"]) {
      stream.addEventListener(eventName, onPolicyEvent);
    }

    fetch(`${API_BASE_URL}/v1/metrics/summary`, {
      cache: "no-store",
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) throw new Error(`Backend returned ${response.status}`);
        return response.json() as Promise<MetricsSummary>;
      })
      .then((data) => {
        if (!active) return;
        setSummary(data);
        setConnection("live");
      })
      .catch(() => {
        if (active && !streamConnected) setConnection("fallback");
      })
      .finally(() => window.clearTimeout(timeout));

    return () => {
      active = false;
      controller.abort();
      window.clearTimeout(timeout);
      stream.close();
    };
  }, []);

  useEffect(() => {
    if (connection !== "fallback") return;
    const interval = window.setInterval(() => {
      const event = replayEvents[replayIndex.current % replayEvents.length];
      replayIndex.current += 1;
      setEvents((current) => [event, ...current].slice(0, 8));
    }, 1800);
    return () => window.clearInterval(interval);
  }, [connection]);

  const statusLabel = connection === "live" ? "Render connected" : connection === "fallback" ? "Local replay" : "Connecting";

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="PAROLE home">
          <span className="brand-mark">P</span>
          <span>PAROLE<span className="brand-dot">.</span></span>
        </a>
        <div className={`connection connection-${connection}`} role="status">
          <span className="status-dot" />
          {statusLabel}
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="eyebrow">POLICY GATEWAY / SYSTEM OVERVIEW</p>
          <h1>Autonomy, <span>within bounds.</span></h1>
          <p className="intro">A live view of policy decisions, risk controls, and gateway health.</p>
        </div>
        <div className="service-card">
          <span className="service-icon">↗</span>
          <div>
            <p className="service-label">Gateway endpoint</p>
            <code>{API_BASE_URL.replace(/^https?:\/\//, "")}</code>
          </div>
        </div>
      </section>

      {connection === "fallback" && (
        <div className="notice" role="status">
          Render is unavailable or waking up. Showing the recorded local replay while the dashboard stays available.
        </div>
      )}

      <section className="metrics" aria-label="Gateway metrics">
        <article className="metric-card">
          <p>Total traces</p>
          <strong>{formatNumber(summary.total_traces_evaluated)}</strong>
          <span>Evaluated actions</span>
        </article>
        <article className="metric-card">
          <p>Blocked threats</p>
          <strong>{formatNumber(summary.zero_day_block_rate_pct, 1)}<small>%</small></strong>
          <span>Adversarial replay rate</span>
        </article>
        <article className="metric-card">
          <p>Safe decision accuracy</p>
          <strong>{formatNumber(summary.safe_auto_grant_accuracy_pct, 2)}<small>%</small></strong>
          <span>Benchmark baseline</span>
        </article>
        <article className="metric-card">
          <p>p95 resolution</p>
          <strong>{formatNumber(summary.p95_latency_ms, 3)}<small> ms</small></strong>
          <span>{summary.capability} capability</span>
        </article>
      </section>

      <section className="content-grid">
        <article className="panel activity-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">DECISION FEED</p>
              <h2>Policy activity</h2>
            </div>
            <span className={`feed-tag ${connection === "live" ? "feed-live" : ""}`}>
              <span className="status-dot" /> {connection === "live" ? "LIVE" : "REPLAY"}
            </span>
          </div>
          <div className="event-list">
            {events.map((event, index) => (
              <div className="event-row" key={`${event.source}-${event.id}-${index}`}>
                <span className={`event-icon ${event.decision === "INTERCEPTED" ? "event-deny" : ""}`}>
                  {event.decision === "INTERCEPTED" ? "×" : "✓"}
                </span>
                <div className="event-main">
                  <strong>{event.label}</strong>
                  <span>{event.tier.replaceAll("_", " ")} · {event.source === "live" ? "Live event" : "Recorded run"}</span>
                </div>
                <div className="event-result">
                  <strong className={event.decision === "INTERCEPTED" ? "text-danger" : ""}>{event.decision}</strong>
                  <span>{formatNumber(event.latency, 3)} ms</span>
                </div>
              </div>
            ))}
          </div>
        </article>

        <aside className="panel breakdown-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">ROUTING</p>
              <h2>Decision tiers</h2>
            </div>
            <span className="muted-label">BENCHMARK</span>
          </div>
          <div className="tier-list">
            {([
              ["Local cache", summary.tier_distribution.tier_0, "tier-cyan"],
              ["Typed risk", summary.tier_distribution.tier_1, "tier-violet"],
              ["Deep synthesis", summary.tier_distribution.tier_2, "tier-amber"],
            ] as const).map(([label, percent, color]) => (
              <div className="tier-item" key={label}>
                <div className="tier-label"><span>{label}</span><strong>{percent}%</strong></div>
                <div className="bar-track"><span className={color} style={{ width: `${Math.min(percent, 100)}%` }} /></div>
              </div>
            ))}
          </div>
          <div className="panel-footnote">
            <span>False positive rate</span>
            <strong>{formatNumber(summary.false_positive_rate_pct, 2)}%</strong>
          </div>
          <div className="panel-footnote">
            <span>Estimated / 1k actions</span>
            <strong>${formatNumber(summary.cost_per_1k_actions_usd, 2)}</strong>
          </div>
        </aside>
      </section>

      <footer>
        <span>PAROLE POLICY GATEWAY</span>
        <span>Fallback replay is for demonstration; decisions are advisory.</span>
      </footer>
    </main>
  );
}
