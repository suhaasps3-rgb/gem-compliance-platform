// src/components/Layout/SplitScreen.jsx
// Resizable split panel with drag divider, minimize toggle, and Lenis smooth scroll on the right panel.
import React, { useRef, useState, useEffect, useCallback } from 'react';
import Lenis from 'lenis';

const MIN_LEFT_PCT = 15;
const MAX_LEFT_PCT = 80;
const DEFAULT_LEFT_PCT = 40;

export default function SplitScreen({ left, right }) {
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
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    return () => lenis.destroy();
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
    <div
      ref={containerRef}
      className="flex flex-1 overflow-hidden"
      style={{ height: 'calc(100vh - 48px)' }}
    >
      {/* ── Left Panel (PDF Viewer) ── */}
      <section
        className="flex flex-col overflow-hidden relative"
        style={{
          width: `${effectivePct}%`,
          transition: isDragging ? 'none' : 'width 0.2s ease',
          minWidth: minimized ? 0 : undefined,
        }}
      >
        {!minimized && (
          <div className="flex flex-col h-full overflow-auto">{left}</div>
        )}
        {/* Transparent drag shield — blocks iframe from stealing mouse events during drag */}
        {isDragging && (
          <div className="absolute inset-0 z-50" style={{ cursor: 'col-resize' }} />
        )}
      </section>

      {/* ── Drag Divider ── */}
      <div
        onMouseDown={onMouseDown}
        className="relative flex items-center justify-center w-2.5 shrink-0 bg-slate-200 hover:bg-blue-200 cursor-col-resize group transition-colors z-10 select-none"
        title="Drag to resize"
      >
        {/* Drag handle dots */}
        <div className="flex flex-col gap-1 items-center">
          {[0,1,2,3,4].map(i => (
            <div key={i} className="w-1 h-1 rounded-full bg-slate-400 group-hover:bg-blue-500 transition-colors" />
          ))}
        </div>

        {/* Minimize / Restore button — sits on the divider */}
        <button
          onMouseDown={e => e.stopPropagation()}
          onClick={handleMinimize}
          title={minimized ? 'Restore PDF panel' : 'Minimize PDF panel'}
          className="absolute top-4 left-1/2 -translate-x-1/2 w-6 h-6 rounded-full bg-white border border-slate-300 shadow-md flex items-center justify-center hover:bg-blue-500 hover:border-blue-500 hover:text-white text-slate-500 transition-all z-20"
        >
          {minimized ? (
            // Right-pointing chevron (expand)
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
            </svg>
          ) : (
            // Left-pointing chevron (collapse)
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
            </svg>
          )}
        </button>
      </div>

      {/* ── Right Panel (Dashboard) with Lenis ── */}
      <section
        ref={rightRef}
        className="flex-1 overflow-y-auto overflow-x-hidden"
        style={{ scrollBehavior: 'auto' }} // Lenis takes over
      >
        <div>
          {right}
        </div>
      </section>
    </div>
  );
}
