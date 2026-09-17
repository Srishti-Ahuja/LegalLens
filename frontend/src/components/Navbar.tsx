import Link from 'next/link';
import Head from 'next/head';
import { Notable } from 'next/font/google';

// Initialize the font
const notable = Notable({
  weight: '400',
  subsets: ['latin'],
  display: 'swap',
});

export default function Navbar() {
  return (
    <nav className="bg-charcoal border-b border-plum-500">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center h-16 items-center">
          <Link
            href="/"
            className={`${notable.className} flex items-center gap-2 text-beige font-bold text-xl focus-visible:ring-2 focus-visible:ring-plum-500 rounded px-2 py-1`}
          >
            <span>Legal Lens</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}
