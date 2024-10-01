import Link from 'next/link'
import React from 'react'
import { Center, Title, Text, Container } from '@mantine/core'
import LoginForm from './components/LoginForm'

const Login = () => {
    return (
        <main className='w-full bg-white h-screen flex flex-col justify-center'>
            <Center>
                <div className='rounded-lg bg-slate-50 border p-20 min-w-[480px]'>
                    <Container fluid p={0}>
                        <Center>
                            <Title>Log In</Title>
                        </Center>
                    </Container>
                    <LoginForm className='mt-4' />
                    <div className='text-center mt-5 text-gray-700'>
                        Don't have an account?{' '}
                        <Link
                            href='/signup'
                            className='text-blue-500 font-semibold'
                        >
                            Sign Up
                        </Link>
                    </div>
                </div>
            </Center>
        </main>
    )
}

export default Login
