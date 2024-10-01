import './globals.css'
import { Inter } from 'next/font/google'

import Providers from './providers/index'
import '@mantine/core/styles.css'
import '@mantine/notifications/styles.css'

const inter = Inter({ subsets: ['latin', 'cyrillic'] })

export const metadata = {
    title: 'AMLRSS',
    description: 'Autonomous Peer Reviewer Selection System',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang='en'>
            <body className={inter.className}>
                <Providers>{children}</Providers>
            </body>
        </html>
    )
}
