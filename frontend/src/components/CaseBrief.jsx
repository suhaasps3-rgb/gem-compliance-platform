import React from 'react';
import { GrowBar, reducedMotion } from '../utils/motion';

/** Scrolls to a section and moves keyboard focus there, so the jump works without a mouse too. */
export function jumpTo(id) {
  const el = typeof document !== 'undefined' ? document.getElementById(id) : null;
  if (!el) return;
  el.scrollIntoView({ behavior: reducedMotion() ? 'auto' : 'smooth', block: 'start' });
  el.setAttribute('tabindex', '-1');
  el.focus({ preventScroll: true });
}

const SEGMENT = {
  PASS: 'bg-ink',
  FAIL: 'bg-red-600',
  UNVERIFIED: 'bg-slate-300',
};

/**
 * "At a glance": how much of the case is actually verified, and the short list of things the
 * officer has to look at, each one a jump to the card that explains it.
 * checks: [{ key, label, status: 'PASS' | 'FAIL' | other }]; attention: [{ id, text, tone: 'bad' | 'warn', target }]
 */
export default function CaseBrief({ checks, attention }) {
  const total = checks.length;
  const passed = checks.filter((c) => c.status === 'PASS').length;
  const failed = checks.filter((c) => c.status === 'FAIL').length;
  const unverified = total - passed - failed;
  const hasAttention = attention.length > 0;

  return (
    <section className="card @container" aria-labelledby="brief-title">
      <div className="card-head border-b border-slate-100">
        <h2 id="brief-title" className="card-title">At a glance</h2>
        <span className="card-note">
          {hasAttention ? `${attention.length} thing${attention.length > 1 ? 's' : ''} to look at` : 'Nothing flagged'}
        </span>
      </div>

      <div className="grid @2xl:grid-cols-[minmax(0,1fr)_minmax(0,1.15fr)]">
        {/* How much is verified */}
        <div className="px-5 py-4 @2xl:border-r border-slate-100">
          <div className="label">Registry checks verified</div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-[36px] leading-none num">{passed}</span>
            <span className="text-[14px] text-slate-500">of {total}</span>
          </div>
          {total > 0 && (
            <div
              className="mt-3 flex gap-1"
              role="img"
              aria-label={`${passed} verified, ${unverified} unverified, ${failed} failed, out of ${total} registry checks`}
            >
              {checks.map((c, i) => (
                <GrowBar
                  key={c.key}
                  delay={0.15 + i * 0.05}
                  title={`${c.label}: ${c.status === 'PASS' ? 'verified' : c.status === 'FAIL' ? 'failed' : 'unverified'}`}
                  className={`h-2 flex-1 rounded-sm ${SEGMENT[c.status] || SEGMENT.UNVERIFIED}`}
                />
              ))}
            </div>
          )}
          <ul className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[12px] text-slate-600">
            <li className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm bg-ink" aria-hidden="true" />{passed} verified</li>
            <li className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm bg-slate-300" aria-hidden="true" />{unverified} unverified</li>
            <li className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm bg-red-600" aria-hidden="true" />{failed} failed</li>
          </ul>
        </div>

        {/* What needs the officer */}
        <div className="px-5 py-4 min-w-0">
          <div className="label">Needs your attention</div>
          {hasAttention ? (
            <ul className="mt-2">
              {attention.map((a) => (
                <li key={a.id} className="border-t border-slate-100 first:border-t-0">
                  <button
                    onClick={() => jumpTo(a.target)}
                    className="w-full min-h-10 py-2 flex items-center gap-3 text-left text-[14px] text-slate-800 hover:text-ink group"
                  >
                    <span
                      className={`w-2 h-2 rounded-full shrink-0 ${a.tone === 'bad' ? 'bg-red-600' : 'bg-amber-600'}`}
                      aria-hidden="true"
                    />
                    <span className="flex-1 min-w-0">{a.text}</span>
                    <svg className="w-3.5 h-3.5 shrink-0 text-slate-400 group-hover:text-ink" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-2 text-[14px] text-slate-700">
              No red flags, conflicts or missing documents. Review the recommendation, then record your decision.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
