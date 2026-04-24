"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity } from "lucide-react";
import { ThemeToggle } from "./theme-toggle";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/predict", label: "Predict" },
  { href: "/models", label: "Models" },
  { href: "/evaluation", label: "Evaluation" },
  { href: "/history", label: "History" },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-6xl items-center mx-auto px-4">
        <Link href="/" className="flex items-center gap-2 mr-8">
          <Activity className="h-5 w-5 text-emerald-500" />
          <span className="font-bold tracking-tight">AMR Predict</span>
        </Link>

        <nav className="flex items-center gap-6 text-sm">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "transition-colors hover:text-foreground",
                pathname === item.href
                  ? "text-foreground font-medium"
                  : "text-muted-foreground"
              )}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="ml-auto">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
