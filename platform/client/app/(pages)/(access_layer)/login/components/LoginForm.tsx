'use client'

import { Button, Center, PasswordInput, TextInput } from '@mantine/core'
import { useForm, isEmail, hasLength } from '@mantine/form'
import { signIn } from 'next-auth/react'

const LoginForm = ({ className }: { className: string }) => {
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: { username: '', password: '' },
    })

    const login = (values: any) => {
        console.log(values)
        signIn('login', {
            ...values,
            callbackUrl: '/dashboard',
        })
    }

    return (
        <form onSubmit={form.onSubmit(login)}>
            <div className='flex-col'>
                <TextInput
                    {...form.getInputProps('username')}
                    key={form.key('username')}
                    mt='lg'
                    placeholder='Username'
                />
                <PasswordInput
                    {...form.getInputProps('password')}
                    key={form.key('password')}
                    mt='lg'
                    placeholder='Password'
                />
                <Button
                    type='submit'
                    mt='lg'
                    fullWidth
                    variant='filled'
                    color='blue'
                >
                    Log In
                </Button>
            </div>
        </form>
    )
}

export default LoginForm
