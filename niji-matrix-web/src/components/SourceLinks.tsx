import { ExternalLink } from "lucide-react";
import { title, type RecordData } from "../data";

export function sourceUrl(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  try {
    const url = new URL(value);
    if (url.protocol === "https:" || url.protocol === "http:") return value;
  } catch {
    // Missing or incomplete source URLs do not get a navigation control.
  }
  return undefined;
}

export function SourceLink({ href, name, label = "查看原文", showLabel = false }: {
  href: string;
  name?: string;
  label?: string;
  showLabel?: boolean;
}) {
  const description = `${label}${name ? `：${name}` : ""}（新标签页打开）`;
  return <a className="source-link" href={href} target="_blank" rel="noopener noreferrer"
    aria-label={description} title={`${description}\n${href}`}>
    {showLabel && <span>{label}</span>}
    <ExternalLink size={14} aria-hidden="true" />
  </a>;
}

export function RecordSourceLinks({ record, lang = "zh", showLabel = false }: {
  record?: RecordData;
  lang?: string;
  showLabel?: boolean;
}) {
  if (!record) return null;
  const links = [
    { href: sourceUrl(record.url), label: "查看原文" },
    { href: sourceUrl(record.source?.url), label: "查看原文" },
    { href: sourceUrl(record.archive_url), label: "查看存档" },
  ].filter((link, i, all) => link.href && all.findIndex(other => other.href === link.href) === i);
  if (!links.length) return null;
  return <span className="source-links">{links.map(link => <SourceLink key={link.href}
    href={link.href!} name={title(record, lang)} label={link.label} showLabel={showLabel} />)}</span>;
}
