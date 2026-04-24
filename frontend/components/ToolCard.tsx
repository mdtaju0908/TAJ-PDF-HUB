 "use client";

import Link from "next/link";
import type { LucideIcon } from "lucide-react";
import {
  Camera,
  Combine,
  Crop,
  Eraser,
  Eye,
  FileArchive,
  FileImage,
  FilePlus,
  FileSignature,
  FileSpreadsheet,
  FileText,
  Hash,
  Layers,
  Lock,
  Minimize2,
  Presentation,
  RotateCw,
  Scissors,
  Search,
  ShieldOff,
  Unlock,
  Wrench
} from "lucide-react";
import { TOOL_DEFINITIONS, type PdfToolId } from "@/lib/tools";
import { cn } from "@/lib/utils";

const iconMap: Record<PdfToolId, LucideIcon> = {
  merge: Combine,
  split: Scissors,
  compress: Minimize2,
  "pdf-to-word": FileText,
  "pdf-to-ppt": FileText,
  "pdf-to-excel": FileSpreadsheet,
  "word-to-pdf": FileText,
  "ppt-to-pdf": Presentation,
  "excel-to-pdf": FileSpreadsheet,
  edit: FilePlus,
  "jpg-to-pdf": FileImage,
  "pdf-to-jpg": FileImage,
  sign: FileSignature,
  repair: Wrench,
  "page-numbers": Hash,
  scan: Camera,
  ocr: Search,
  compare: Eye,
  redact: ShieldOff,
  crop: Crop,
  watermark: Layers,
  rotate: RotateCw,
  "html-to-pdf": FileText,
  unlock: Unlock,
  protect: Lock,
  organize: Layers,
  "pdf-a": FileArchive,
  "bg-remover": Eraser
};

interface ToolCardProps {
  toolId: PdfToolId;
}

export function ToolCard({ toolId }: ToolCardProps) {
  const tool = TOOL_DEFINITIONS.find(t => t.id === toolId);
  if (!tool) return null;
  const Icon = iconMap[tool.id];
  if (!Icon) return null;
  return (
    <Link href={`/tools/${tool.id}`} className="group block focus:outline-none">
      <div
        className={cn(
          "h-full cursor-pointer overflow-hidden rounded-2xl border p-5 shadow-[0_10px_30px_-18px_rgba(15,23,42,0.35)] transition-all duration-300 ease-out",
          "hover:-translate-y-1 hover:shadow-[0_16px_40px_-18px_rgba(79,70,229,0.35)]",
          "focus-visible:ring-2 focus-visible:ring-indigo-400/50",
          tool.borderColor ?? "border-slate-200",
          tool.bgLight ?? "bg-white"
        )}
      >
        <div className={cn("mb-4 h-1 w-full rounded-full bg-gradient-to-r", tool.gradient)} />
        <div className="relative flex h-full flex-col">
          <div className="mb-4 flex items-center justify-between">
            <div
              className={cn(
                "rounded-xl border border-slate-200/80 p-2.5 shadow-sm backdrop-blur-sm transition-all",
                "ring-1 ring-white/70 group-hover:scale-105",
                tool.iconBg ?? "bg-white/80"
              )}
            >
              <Icon className={cn("h-6 w-6", tool.iconColor ?? "text-slate-800")} strokeWidth={2.3} />
            </div>
          </div>
          <h3 className="text-xl font-semibold tracking-tight text-slate-900">{tool.title}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600 line-clamp-2">{tool.description}</p>
        </div>
      </div>
    </Link>
  );
}

interface ToolGridProps {
  limit?: number;
}

export function ToolGrid({ limit }: ToolGridProps) {
  const tools = limit ? TOOL_DEFINITIONS.slice(0, limit) : TOOL_DEFINITIONS;

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {tools.map(tool => (
        <ToolCard key={tool.id} toolId={tool.id} />
      ))}
    </div>
  );
}
