"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, History } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export function HeroSection() {
  return (
    <section className="flex flex-col items-center justify-center text-center py-20 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Badge variant="secondary" className="mb-4">
          ML + DL Powered
        </Badge>
      </motion.div>

      <motion.h1
        className="text-4xl md:text-6xl font-bold tracking-tight bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent max-w-4xl"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        Multi-Drug AMR Prediction System
      </motion.h1>

      <motion.p
        className="text-lg text-muted-foreground max-w-2xl mt-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        Predict antibiotic resistance for every drug against a microbe.
        Enter patient data, select the microbe, and get an instant full
        resistance report with best drug recommendations.
      </motion.p>

      <motion.div
        className="flex gap-4 mt-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Link href="/predict" className={cn(buttonVariants({ size: "lg" }), "gap-2")}>
          Start Prediction
          <ArrowRight className="h-4 w-4" />
        </Link>
        <Link href="/history" className={cn(buttonVariants({ variant: "outline", size: "lg" }), "gap-2")}>
          <History className="h-4 w-4" />
          View History
        </Link>
      </motion.div>
    </section>
  );
}
