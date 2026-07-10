import React from 'react'

export const metadata = {
  title: 'Group 6 Supabase Demo',
  description: 'Supabase integration demo',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  )
}
