import { useEffect } from 'react';

const FOCUSABLE = 'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

/**
 * While `active`, moves focus into the open modal dialog, keeps Tab inside it, and puts focus
 * back on whatever opened it when it closes.
 */
export default function useDialogFocus(active = true) {
  useEffect(() => {
    if (!active) return undefined;
    const opener = document.activeElement;
    const dialog = () => document.querySelector('[role="dialog"][aria-modal="true"]');
    const first = dialog()?.querySelector(FOCUSABLE);
    if (first) first.focus();

    const onKey = (e) => {
      if (e.key !== 'Tab') return;
      const d = dialog();
      if (!d) return;
      const items = Array.from(d.querySelectorAll(FOCUSABLE));
      if (!items.length) return;
      const head = items[0];
      const tail = items[items.length - 1];
      if (e.shiftKey && document.activeElement === head) { e.preventDefault(); tail.focus(); }
      else if (!e.shiftKey && document.activeElement === tail) { e.preventDefault(); head.focus(); }
      else if (!d.contains(document.activeElement)) { e.preventDefault(); head.focus(); }
    };
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      if (opener && typeof opener.focus === 'function' && document.contains(opener)) opener.focus();
    };
  }, [active]);
}
