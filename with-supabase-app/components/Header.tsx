"use client";

import { AuthButton } from "@/components/AuthComponents/auth-button";
import Link from "next/link";
import { useEffect, useState } from "react";
import Image from "next/image";

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      setIsScrolled(scrollTop > 20);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ease-in-out ${
        isScrolled
          ? "bg-background/80 backdrop-blur-md border-b border-border/50 shadow-sm"
          : "bg-transparent"
      }`}
    >
      <nav
        className={`w-full flex justify-center transition-all duration-300 ease-in-out ${
          isScrolled ? "h-14" : "h-16"
        }`}
      >
        <div className="w-full max-w-5xl flex justify-between items-center px-5 transition-all duration-300 ease-in-out">
          <div className="flex gap-5 items-center font-semibold">
            <Link
              href={"/"}
              className={`transition-all duration-300 ease-in-out ${
                isScrolled ? "text-lg" : "text-xl"
              } hover:text-primary`}
            >
              <Image src="/logo.png" alt="PocketBroker" width={32} height={32} />
              
            </Link>
          </div>
          
          {/* Center Navigation Links - Hidden on Mobile */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              href="/onboarding"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isScrolled ? "text-foreground/80" : "text-foreground"
              }`}
            >
              Onboarding
            </Link>
            {/* <Link
              href="/portfolio"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isScrolled ? "text-foreground/80" : "text-foreground"
              }`}
            >
              Portfolio
            </Link>
            <Link
              href="/analytics"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isScrolled ? "text-foreground/80" : "text-foreground"
              }`}
            >
              Analytics
            </Link>
            <Link
              href="/settings"
              className={`text-sm font-medium transition-colors hover:text-primary ${
                isScrolled ? "text-foreground/80" : "text-foreground"
              }`}
            >
              Settings
            </Link> */}
          </nav>
          
          <div className={`transition-all duration-300 ease-in-out ${
            isScrolled ? "scale-95" : "scale-100"
          }`}>
            <AuthButton />
          </div>
        </div>
      </nav>
    </header>
  );
}
