import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PAROLE | Policy Gateway",
  description: "Live and replay telemetry for the PAROLE policy gateway.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
