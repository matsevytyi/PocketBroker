import { Hero } from "@/components/hero";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center pt-16">
      <div className="flex-1 w-full flex flex-col gap-20 items-center">
        <div className="flex-1 flex flex-col gap-20 max-w-7xl p-5">
          <Hero />
        </div>
      </div>
    </main>
  );
}
