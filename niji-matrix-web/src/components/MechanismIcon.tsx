/** Shared monochrome visual vocabulary for the four canonical mechanisms.
 * Decorative by design: every usage keeps the corresponding text label.
 */
export function MechanismIcon({ id, size = 18 }: { id: string; size?: number }) {
  const drawings = {
    'NM-DO': <>
      <path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8zM14 3v5h5M8 10h4M8 18h5" />
      <rect x="3" y="12" width="18" height="4" rx="1" />
      <path d="m7 12-2 4m7-4-2 4m7-4-2 4" />
    </>,
    'NM-BT': <>
      <path d="M17.6 5.6a9 9 0 1 0 0 12.8M14.8 8.4a5 5 0 1 0 0 7.2" />
      <path d="m11 12 7-7m-7 7 7 7" strokeDasharray="2 3" />
      <circle cx="11" cy="12" r="1" />
      <circle cx="20" cy="12" r="2" />
    </>,
    'NM-FD': <>
      <path d="M3 7c3-2 5-2 9 0 4-2 6-2 9 0l-1 7c-.5 3-4 4-6 1l-2-2-2 2c-2 3-5.5 2-6-1z" />
      <path d="M6 10c1-1 3-1 4 0-1 2-3 2-4 0Zm8 0c1-1 3-1 4 0-1 2-3 2-4 0ZM3 8 1 6m20 2 2-2" />
    </>,
    'NM-ST': <>
      <circle cx="8" cy="8" r="5" />
      <path d="M8 5v3l2 1M14 9l4-2M11 14l1 4m3-6 4 5" strokeDasharray="2 2" />
      <circle cx="20" cy="6" r="1.5" />
      <circle cx="12" cy="21" r="1.5" />
      <circle cx="21" cy="19" r="1.5" />
    </>,
  };
  const drawing = drawings[id as keyof typeof drawings];
  if (!drawing) return null;
  return <svg className="mechanism-icon" data-mechanism={id} width={size} height={size}
    viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"
    strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
    {drawing}
  </svg>;
}
