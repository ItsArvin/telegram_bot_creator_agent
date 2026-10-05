import type { Metadata } from "next";
import "./globals.css";
export const metadata:Metadata={title:"Agentic Telegram Bot Builder",description:"Build and test Telegram bots using natural language."};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
