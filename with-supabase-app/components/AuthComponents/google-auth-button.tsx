"use client";

import { createClient } from "@/lib/supabase/client";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import Image from "next/image";

interface GoogleAuthButtonProps {
  className?: string;
  variant?: "default" | "outline" | "secondary" | "ghost" | "link" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
  children?: React.ReactNode;
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

export function GoogleAuthButton({
  className,
  variant = "outline",
  size = "default",
  children = "Continue with Google",
  onSuccess,
  onError,
}: GoogleAuthButtonProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleGoogleAuth = async () => {
    setIsLoading(true);
    const supabase = createClient();

    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });

      if (error) {
        throw error;
      }
      
      // Note: OAuth redirects will handle the success case
      // This callback is mainly for error handling
      onSuccess?.();
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "An error occurred";
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      type="button"
      variant={variant}
      size={size}
      className={className}
      onClick={handleGoogleAuth}
      disabled={isLoading}
    >
      {isLoading ? (
        "Signing in..."
      ) : (
        <div className="flex items-center gap-2">
          <Image
            src="/google-icon-logo-svgrepo-com.svg"
            alt="Google"
            width={20}
            height={20}
            className="w-5 h-5"
          />
          {children}
        </div>
      )}
    </Button>
  );
}
