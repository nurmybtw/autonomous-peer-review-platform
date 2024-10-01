'use client'

import { Button, Group } from '@mantine/core'
import Link from 'next/link'
import React, { useState } from 'react'

const Header = () => {
    const [page, setPage] = useState('dashboard')
    return (
        <div className='h-16 flex'>
            <Group justify='space-between' className='w-full'>
                <Group gap='xs'>
                    <Button
                        variant={page == 'dashboard' ? 'filled' : 'subtle'}
                        // color='dark'
                        component={Link}
                        onClick={() => setPage('dashboard')}
                        href='/dashboard'
                    >
                        Dashboard
                    </Button>
                    <Button
                        variant={page == 'submissions' ? 'filled' : 'subtle'}
                        // color='dark'
                        component={Link}
                        onClick={() => setPage('submissions')}
                        href='/submissions'
                    >
                        Submissions
                    </Button>
                    <Button
                        variant={page == 'reviews' ? 'filled' : 'subtle'}
                        // color='dark'
                        component={Link}
                        onClick={() => setPage('reviews')}
                        href='/reviews'
                    >
                        Reviews
                    </Button>
                </Group>
                <Button variant='subtle'>My Profile</Button>
            </Group>
        </div>
    )
}

export default Header
