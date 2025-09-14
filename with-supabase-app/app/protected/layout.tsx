export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="min-h-screen flex flex-col items-center">
      <div className="flex-1 w-full flex flex-col gap-8 md:gap-12 lg:gap-20 items-center pt-20 md:pt-24 lg:pt-16 px-4 md:px-6 lg:px-8">
          {children}
      </div>
    </main>
  );
}
