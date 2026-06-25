import type { Metadata, Viewport } from "next"
import { Inter, JetBrains_Mono } from "next/font/google"
import "./globals.css"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
})

export const metadata: Metadata = {
  title: "Cyber-SH — Your Personal Offline AI",
  description:
    "Cyber-SH is an advanced, fully offline AI that runs locally on your machine. Private neural core, vibe coding engine, and terminal execution — all without the cloud.",
  keywords: ["offline AI", "local AI", "private AI", "Cyber-SH", "neural agent", "AI coding"],
  openGraph: {
    title: "Cyber-SH — Your Personal Offline AI",
    description: "An advanced, fully offline AI that runs locally. Total privacy, real power.",
    type: "website",
  },
}

export const viewport: Viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable} bg-background`}>
      <body className="font-sans antialiased bg-background text-foreground">{children}</body>
    </html>
  )
}
