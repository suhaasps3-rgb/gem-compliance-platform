// Small motion layer (GSAP). Rules: feedback not decoration, under 400ms except the count-up,
// transforms and opacity only, and nothing moves when the user prefers reduced motion.
import React, { useLayoutEffect, useRef } from 'react';
import gsap from 'gsap';

export const reducedMotion = () =>
  typeof window !== 'undefined' &&
  typeof window.matchMedia === 'function' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/**
 * Wraps the loaded case. On mount (which happens each time a bidder's data lands after the
 * skeleton) its direct children settle in with a short stagger.
 */
export function RevealOnMount({ children, ...props }) {
  const ref = useRef(null);
  useLayoutEffect(() => {
    const root = ref.current;
    if (!root || reducedMotion()) return undefined;
    const ctx = gsap.context(() => {
      gsap.from(root.children, {
        autoAlpha: 0,
        y: 8,
        duration: 0.28,
        stagger: 0.04,
        ease: 'power2.out',
        clearProps: 'opacity,visibility,transform',
      });
    }, root);
    return () => ctx.revert();
  }, []);
  return <div ref={ref} {...props}>{children}</div>;
}

/** A number that counts from its previous value (0 on first show) to `value`. */
export function CountUp({ value, decimals = 0, duration = 0.7 }) {
  const ref = useRef(null);
  const prev = useRef(0);
  useLayoutEffect(() => {
    const el = ref.current;
    const to = Number(value);
    if (!el) return undefined;
    const fmt = (v) => v.toFixed(decimals);
    if (!Number.isFinite(to) || reducedMotion()) {
      el.textContent = Number.isFinite(to) ? fmt(to) : String(value);
      prev.current = Number.isFinite(to) ? to : 0;
      return undefined;
    }
    const state = { v: prev.current };
    el.textContent = fmt(state.v);
    prev.current = to;
    const tween = gsap.to(state, {
      v: to,
      duration,
      ease: 'power2.out',
      onUpdate: () => { el.textContent = fmt(state.v); },
      onComplete: () => { el.textContent = fmt(to); },
    });
    return () => { tween.kill(); el.textContent = fmt(to); };
  }, [value, decimals, duration]);
  // No React children: the text is written by the effect so React never fights the tween.
  return <span ref={ref} />;
}

/** A bar fill that grows from the left (scaleX, not width, so it stays on the compositor). */
export function GrowBar({ delay = 0.1, ...props }) {
  const ref = useRef(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el || reducedMotion()) return undefined;
    const ctx = gsap.context(() => {
      gsap.from(el, { scaleX: 0, transformOrigin: '0 50%', duration: 0.6, delay, ease: 'power2.out', clearProps: 'transform' });
    }, el);
    return () => ctx.revert();
  }, [delay]);
  return <div ref={ref} {...props} />;
}
