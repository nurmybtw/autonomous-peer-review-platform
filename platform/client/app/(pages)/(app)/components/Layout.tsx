'use client'

import { Button, Group, Stack, AppShell, Title, Flex } from '@mantine/core'
import {
    IconFileLike,
    IconFileUpload,
    IconHome,
    IconLogout,
    IconSettings,
} from '@tabler/icons-react'
import Link from 'next/link'
import React, { useEffect, useState } from 'react'
import { signOut } from 'next-auth/react'
import { usePathname } from 'next/navigation'

const Layout = ({ children }: { children: React.ReactNode }) => {
    const pathname = usePathname()
    const [page, setPage] = useState(pathname.split('/')[1])
    useEffect(() => {
        setPage(pathname.split('/')[1])
    }, [pathname])
    return (
        <AppShell
            navbar={{
                width: 240,
                breakpoint: 'sm',
            }}
            padding='md'
        >
            <AppShell.Navbar p='md'>
                <div className='flex flex-col h-screen'>
                    <Title order={2} mb={20}>
                        PeerRev
                    </Title>
                    <div className='flex flex-col grow justify-between'>
                        <Stack gap='sm'>
                            <Button
                                variant={
                                    page == 'dashboard' ? 'filled' : 'subtle'
                                }
                                component={Link}
                                onClick={() => setPage('dashboard')}
                                href='/dashboard'
                                leftSection={<IconHome size={20} />}
                                justify='start'
                                color={page == 'dashboard' ? 'blue' : 'dark'}
                            >
                                Dashboard
                            </Button>
                            <Button
                                variant={
                                    page == 'submissions' ? 'filled' : 'subtle'
                                }
                                leftSection={<IconFileUpload size={20} />}
                                justify='start'
                                component={Link}
                                onClick={() => setPage('submissions')}
                                href='/submissions'
                                color={page == 'submissions' ? 'blue' : 'dark'}
                            >
                                Submissions
                            </Button>
                            <Button
                                variant={
                                    page == 'review_requests' ||
                                    page == 'submit_review'
                                        ? 'filled'
                                        : 'subtle'
                                }
                                leftSection={<IconFileLike size={20} />}
                                justify='start'
                                component={Link}
                                onClick={() => setPage('reviews')}
                                href='/reviews'
                                color={
                                    page == 'review_requests' ||
                                    page == 'submit_review'
                                        ? 'blue'
                                        : 'dark'
                                }
                            >
                                Reviews
                            </Button>
                        </Stack>
                        <Stack gap='sm'>
                            <Button
                                variant='subtle'
                                leftSection={<IconSettings size={20} />}
                                justify='start'
                                color='dark'
                                onClick={() => {}}
                            >
                                Settings
                            </Button>
                            <Button
                                variant='subtle'
                                leftSection={<IconLogout size={20} />}
                                justify='start'
                                color='dark'
                                onClick={() =>
                                    signOut({ callbackUrl: '/login' })
                                }
                            >
                                Log out
                            </Button>
                        </Stack>
                    </div>
                </div>
            </AppShell.Navbar>
            <AppShell.Main>{children}</AppShell.Main>
        </AppShell>
    )
}

export default Layout
