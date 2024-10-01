import React from 'react'
import { Center, Title, Button } from '@mantine/core'
import Link from 'next/link'

const Home = () => {
    return (
        <Center className='h-screen'>
            <div className='flex-col'>
                <Title>PeerRev</Title>
                <Button
                    variant='light'
                    color='dark'
                    component={Link}
                    href='/login'
                    fullWidth
                    className='mt-5'
                >
                    Log In
                </Button>
                <Button
                    variant='light'
                    color='dark'
                    component={Link}
                    href='/signup'
                    fullWidth
                    className='mt-5'
                >
                    Sign Up
                </Button>
            </div>
        </Center>
    )
}

export default Home
