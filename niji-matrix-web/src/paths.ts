/** Resolve exported data and case material beneath the deployed site prefix. */
export function publicAssetUrl(path: string): string {
  const base = import.meta.env.BASE_URL;
  if (/^(?:https?:)?\/\//.test(path)) return path;
  if (base !== '/' && path.startsWith(base)) return path;
  return `${base}${path.replace(/^\/+/, '')}`;
}
