"use client";

import { usePathname } from "next/navigation";
import { Footer } from "./footer";

export function ConditionalFooter() {
  const pathname = usePathname();
  
  // Don't show footer on the home page
  if (pathname === "/") {
    return null;
  }
  
  return <Footer />;
}
