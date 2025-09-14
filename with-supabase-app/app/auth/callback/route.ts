import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { type NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/";

  if (code) {
    const supabase = await createClient();
    
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    
    if (!error) {
      // Get the current user
      const { data: { user } } = await supabase.auth.getUser();
      
      if (user) {
        // Check if user has completed onboarding
        const { data: profile } = await supabase
          .from('profiles')
          .select('onboarding_completed')
          .eq('id', user.id)
          .single();
        
        // If no profile exists or onboarding is not completed, redirect to onboarding
        if (!profile || !profile.onboarding_completed) {
          redirect('/onboarding');
        } else {
          // Onboarding completed, redirect to protected area
          redirect('/protected');
        }
      }
    }
  }

  // If there's an error or no code, redirect to login
  redirect('/auth/login');
}
