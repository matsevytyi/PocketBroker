import { ThemeSwitcher } from "@/components/AuthComponents/theme-switcher";
import Link from "next/link";

export function Footer() {
  return (
    <footer className="w-full border-t border-border/50 bg-background/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          {/* Left - Brand */}
          <div className="flex flex-col items-center md:items-start gap-4">
            <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition-colors">
              PocketBroker
            </Link>
            <p className="text-sm text-muted-foreground text-center md:text-left max-w-xs">
              Your AI voice agent for smarter crypto trading decisions.
            </p>
          </div>

          {/* Center - Links */}
          <div className="flex flex-wrap items-center justify-center gap-8 text-sm">
            <Link 
              href="/about" 
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              About
            </Link>
            <Link 
              href="/features" 
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              Features
            </Link>
            <Link 
              href="/pricing" 
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              Pricing
            </Link>
            <Link 
              href="/contact" 
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              Contact
            </Link>
          </div>

          {/* Right - Theme Switcher */}
          <div className="flex items-center gap-4">
            <ThemeSwitcher />
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-border/30">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
            <p>© 2024 PocketBroker. All rights reserved.</p>
            <div className="flex items-center gap-6">
              <Link 
                href="/privacy" 
                className="hover:text-foreground transition-colors"
              >
                Privacy Policy
              </Link>
              <Link 
                href="/terms" 
                className="hover:text-foreground transition-colors"
              >
                Terms of Service
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
