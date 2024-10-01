'use client'

import { Button, Center, PasswordInput, TextInput } from '@mantine/core'
import { useForm, isEmail, hasLength } from '@mantine/form'
import { signIn } from 'next-auth/react'

const SignupForm = ({ className }: { className: string }) => {
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            username: '',
            email: '',
            password: '',
            first_name: '',
            last_name: '',
        },
        validate: {
            email: hasLength({ min: 3 }, 'Must be at least 3 characters'),
            password: hasLength({ min: 3 }, 'Must be at least 3 characters'),
        },
    })

    const signup = (values: any) => {
        signIn('signup', {
            ...values,
            callbackUrl: '/dashboard',
        })
    }

    return (
        <form onSubmit={form.onSubmit(signup)}>
            <div className='flex-col'>
                <TextInput
                    {...form.getInputProps('username')}
                    key={form.key('username')}
                    mt='lg'
                    placeholder='Username'
                />
                <TextInput
                    {...form.getInputProps('email')}
                    key={form.key('email')}
                    mt='lg'
                    placeholder='Email address'
                />
                <TextInput
                    {...form.getInputProps('first_name')}
                    key={form.key('first_name')}
                    mt='lg'
                    placeholder='First Name'
                />
                <TextInput
                    {...form.getInputProps('last_name')}
                    key={form.key('last_name')}
                    mt='lg'
                    placeholder='Last Name'
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
                    Sign Up
                </Button>
            </div>
        </form>
    )
}

export default SignupForm
