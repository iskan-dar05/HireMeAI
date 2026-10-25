import { Analytics } from "@vercel/analytics/next";
import type { Metadata, Viewport } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import { ApiTokenProvider } from "@/components/provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "HireMeAI — Your CV, better represented",
  description: "Create, tailor, and improve your CV with HireMeAI.",
  generator: "v0.app",
  icons: {
    icon: [
      {
        url: "/icon-light-32x32.png",
        media: "(prefers-color-scheme: light)",
      },
      {
        url: "/icon-dark-32x32.png",
        media: "(prefers-color-scheme: dark)",
      },
      {
        url: "/icon.svg",
        type: "image/svg+xml",
      },
    ],
    apple: "/apple-icon.png",
  },
};

export const viewport: Viewport = {
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "white" },
    { media: "(prefers-color-scheme: dark)", color: "black" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="antialiased">
          <ApiTokenProvider>{children}</ApiTokenProvider>
          {process.env.NODE_ENV === "production" && <Analytics />}
        </body>
      </html>
    </ClerkProvider>
  );
}
