import './globals.css';
import type { Metadata } from 'next';
import Navbar from '../components/Navbar';

export const metadata: Metadata = {
  title: 'LegalLens - Document Assistant',
  description: 'GenAI Legal Information & Document Assistant',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 flex flex-col">
        <div className="bg-amber-100 text-amber-900 px-4 py-2 text-sm text-center font-medium" role="alert">
          Legal Information Tool: This software provides document analysis, not formal legal advice.
        </div>
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
