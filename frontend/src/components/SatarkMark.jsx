import React from 'react';

/**
 * SATARK means "vigilant". The mark is an open eye: the almond is the officer's scrutiny,
 * the iris is the one data hue the rest of the interface reserves for evidence.
 */
export default function SatarkMark({ size = 22, onDark = false }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true" className="shrink-0">
      <path
        d="M2 12c2.6-4.6 6-7 10-7s7.4 2.4 10 7c-2.6 4.6-6 7-10 7S4.6 16.6 2 12Z"
        stroke={onDark ? '#ffffff' : '#0a0a0a'}
        strokeWidth="1.7"
        strokeLinejoin="round"
      />
      <circle cx="12" cy="12" r="3.3" fill={onDark ? '#6aa5f5' : '#1d5fbf'} />
    </svg>
  );
}
