import Link from 'next/link'
import React from 'react'
import { Center, Title, Text, Container } from '@mantine/core'
import SignupForm from './components/SignupForm'

const Signup = () => {
    return (
        <main className='w-full bg-white h-screen flex flex-col justify-center'>
            <Center>
                <div className='rounded-lg bg-slate-100 border p-20 min-w-[480px]'>
                    <Container fluid p={0}>
                        <Center>
                            <Title>Sign Up</Title>
                        </Center>
                    </Container>
                    <SignupForm className='mt-4' />
                    <div className='text-center mt-5 text-gray-700'>
                        Already have an account?{' '}
                        <Link
                            href='/login'
                            className='text-blue-500 font-semibold'
                        >
                            Login
                        </Link>
                    </div>
                </div>
            </Center>
        </main>
    )
}

export default Signup
