// src/components/Layout/SplitScreen.jsx
// Resizable split panel with drag divider, minimize toggle, and Lenis smooth scroll on the right panel.
// Desktop: documents on a white sheet at the left, the case on the page ground at the right.
// Phone: one pane at a time, chosen from the bottom tab bar (state lives in App).
import React, { useRef, useState, useEffect, useCallback } from 'react';
import Lenis from 'lenis';

const MIN_LEFT_PCT = 15;
const MAX_LEFT_PCT = 80;
const DEFAULT_LEFT_PCT = 40;

export default function SplitScreen({ left, right, mobilePane = 'case' }) {
  const [leftPct, setLeftPct] = useState(DEFAULT_LEFT_PCT);
  const [minimized, setMinimized] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const prevPct = useRef(DEFAULT_LEFT_PCT);
  const containerRef = useRef(null);
  const rightRef = useRef(null);
  const dragging = useRef(false);
  const lenisRef = useRef(null);

  // ── Lenis smooth scroll on the right panel ──
  useEffect(() => {
    if (!rightRef.current) return;
    const lenis = new Lenis({
      wrapper: rightRef.current,
      content: rightRef.current.firstElementChild,
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      smoothWheel: true,
    });
    lenisRef.current = lenis;
    let frame;
    function raf(time) { lenis.raf(time); frame = requestAnimationFrame(raf); }
    frame = requestAnimationFrame(raf);
    return () => { cancelAnimationFrame(frame); lenis.destroy(); };
  }, []);

  // ── Drag logic ──
  const onMouseDown = useCallback((e) => {
    e.preventDefault();
    dragging.current = true;
    setIsDragging(true);
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  }, []);

  useEffect(() => {
    const onMouseMove = (e) => {
      if (!dragging.current || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const raw = ((e.clientX - rect.left) / rect.width) * 100;
      const clamped = Math.max(MIN_LEFT_PCT, Math.min(MAX_LEFT_PCT, raw));
      setLeftPct(clamped);
      setMinimized(false);
    };
    const onMouseUp = () => {
      if (!dragging.current) return;
      dragging.current = false;
      setIsDragging(false);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  }, []);

  // ── Minimize / restore ──
  const handleMinimize = () => {
    if (minimized) {
      setMinimized(false);
      setLeftPct(prevPct.current);
    } else {
      prevPct.current = leftPct;
      setMinimized(true);
    }
  };

  const effectivePct = minimized ? 0 : leftPct;

  return (
    <div className="flex flex-col flex-1 min-h-0">
      <div
        ref={containerRef}
        className="flex flex-1 min-h-0 overflow-hidden px-2 pb-2 pt-2 md:pt-0 md:px-2"
      >
        {/* ── Left Panel (PDF Viewer): a white sheet ── */}
        <section
          aria-label="Documents"
          className={`${mobilePane === 'docs' ? 'flex' : 'hidden'} md:flex flex-col overflow-hidden relative bg-sheet border border-slate-200 rounded-lg w-full md:[width:var(--left-w)]`}
          style={{
            '--left-w': `${effectivePct}%`,
            transition: isDragging ? 'none' : 'width 0.2s ease',
            minWidth: minimized ? 0 : undefined,
            borderWidth: minimized ? 0 : undefined,
          }}
        >
          {!minimized && (
            <div className="flex flex-col h-full overflow-auto">{left}</div>
          )}
          {/* Transparent drag shield: blocks iframe from stealing mouse events during drag */}
          {isDragging && (
            <div className="absolute inset-0 z-50" style={{ cursor: 'col-resize' }} />
          )}
        </section>

        {/* ── Drag Divider ── */}
        <div
          onMouseDown={onMouseDown}
          className="hidden md:flex relative items-center justify-center w-3 shrink-0 cursor-col-resize group select-none"
          title="Drag to resize"
        >
          <div className="h-10 w-1 rounded-full bg-slate-300 group-hover:bg-slate-400 transition-colors" />

          {/* Minimize / Restore button: sits on the divider */}
          <button
            onMouseDown={e => e.stopPropagation()}
            onClick={handleMinimize}
            title={minimized ? 'Show documents' : 'Hide documents'}
            aria-label={minimized ? 'Show documents' : 'Hide documents'}
            className="absolute top-3 left-1/2 -translate-x-1/2 w-6 h-6 rounded-full bg-sheet border border-slate-300 flex items-center justify-center text-slate-600 hover:bg-slate-100 hover:text-ink transition-colors z-20"
          >
            {minimized ? (
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M9 5l7 7-7 7" />
              </svg>
            ) : (
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M15 19l-7-7 7-7" />
              </svg>
            )}
          </button>
        </div>

        {/* ── Right Panel (Dashboard) with Lenis ── */}
        <section
          ref={rightRef}
          aria-label="Case review"
          className={`${mobilePane === 'case' ? 'block' : 'hidden'} md:block flex-1 min-w-0 overflow-y-auto overflow-x-hidden overscroll-contain`}
          style={{ scrollBehavior: 'auto' }} // Lenis takes over
        >
          <div>
            {right}
          </div>
        </section>
      </div>
    </div>
  );
}
