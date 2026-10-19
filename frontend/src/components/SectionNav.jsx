import React, { useEffect, useRef, useState } from 'react';
import { jumpTo } from './CaseBrief';

/**
 * Sticky jump bar for the long case pane. Lists only the sections that are on screen right now
 * and underlines the one being read.
 */
export default function SectionNav({ sections }) {
  const navRef = useRef(null);
  const [present, setPresent] = useState([]);
  const [active, setActive] = useState(null);

  useEffect(() => {
    const nav = navRef.current;
    const scroller = nav?.closest('[aria-label="Case review"]') || document.scrollingElement;
    if (!nav || !scroller) return undefined;
    let frame = 0;

    const measure = () => {
      frame = 0;
      const found = sections.filter((s) => {
        const el = document.getElementById(s.id);
        return el && el.offsetHeight > 0;
      });
      setPresent((prev) => (prev.map((s) => s.id).join() === found.map((s) => s.id).join() ? prev : found));
      const top = scroller.getBoundingClientRect ? scroller.getBoundingClientRect().top : 0;
      let current = found[0]?.id ?? null;
      for (const s of found) {
        if (document.getElementById(s.id).getBoundingClientRect().top - top <= 96) current = s.id;
      }
      setActive(current);
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(measure); };

    measure();
    scroller.addEventListener('scroll', schedule, { passive: true });
    // Sections appear and disappear as documents are uploaded or cleared.
    const mo = new MutationObserver(schedule);
    mo.observe(scroller, { childList: true, subtree: true });
    window.addEventListener('resize', schedule);
    return () => {
      if (frame) cancelAnimationFrame(frame);
      scroller.removeEventListener('scroll', schedule);
      mo.disconnect();
      window.removeEventListener('resize', schedule);
    };
  }, [sections]);

  return (
    <nav
      ref={navRef}
      aria-label="Jump to section"
      className="sticky top-0 z-20 -mx-4 md:-mx-6 px-4 md:px-6 bg-ground border-b border-slate-200"
    >
      <ul className="flex gap-4 overflow-x-auto overflow-y-hidden [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {present.map((s) => (
          <li key={s.id} className="shrink-0">
            <button
              onClick={() => jumpTo(s.id)}
              aria-current={active === s.id ? 'true' : undefined}
              className={`h-10 text-[13px] whitespace-nowrap border-b-2 -mb-px transition-colors ${
                active === s.id ? 'text-ink font-medium border-ink' : 'text-slate-500 hover:text-ink border-transparent'
              }`}
            >
              {s.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
