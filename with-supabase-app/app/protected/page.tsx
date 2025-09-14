import { redirect } from "next/navigation";

import { createClient } from "@/lib/supabase/server";
import { InfoIcon } from "lucide-react";

export default async function ProtectedPage() {
  const supabase = await createClient();

  const { data, error } = await supabase.auth.getClaims();
  if (error || !data?.claims) {
    redirect("/auth/login");
  }

  // Check if user has completed onboarding
  const { data: profile } = await supabase
    .from('profiles')
    .select('onboarding_completed')
    .eq('id', data.claims.sub)
    .single();

  // If no profile exists or onboarding is not completed, redirect to onboarding
  if (!profile || !profile.onboarding_completed) {
    redirect('/onboarding');
  }

  return (
    <div className="flex-1 w-full max-w-4xl flex flex-col gap-6 md:gap-8 lg:gap-12">
      <div className="w-full">
        <div className="bg-accent text-sm p-3 px-4 md:px-5 rounded-md text-foreground flex gap-3 items-center">
          <InfoIcon size="16" strokeWidth={2} />
          <span className="text-xs md:text-sm">Welcome to PocketBroker! This is your protected dashboard.</span>
        </div>
      </div>
      <div className="flex flex-col gap-2 items-start w-full">
        <h2 className="font-bold text-xl md:text-2xl mb-3 md:mb-4">Your Profile</h2>
        <pre className="text-xs font-mono p-3 rounded border max-h-32 md:max-h-40 lg:max-h-48 overflow-auto w-full break-words whitespace-pre-wrap">
          {JSON.stringify(data.claims, null, 2)}
        </pre>
      </div>
      <div className="w-full">
        <h2 className="font-bold text-xl md:text-2xl mb-3 md:mb-4">Dashboard</h2>
        <p className="text-muted-foreground text-sm md:text-base">
          Your PocketBroker dashboard is ready. Start exploring your portfolio and trading features.
        </p>
      </div>
    </div>
  );
}
