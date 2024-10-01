import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { signin } from '@/app/api/authAPI'
import { create } from '@/app/api/usersAPI'

export const authOptions: NextAuthOptions = {
    providers: [
        CredentialsProvider({
            name: 'credentials',
            id: 'login',
            credentials: {
                email: { label: 'username', type: 'text' },
                password: { label: 'password', type: 'password' },
            },
            async authorize(credentials) {
                const data = await signin(credentials)
                return data
            },
        }),
        CredentialsProvider({
            name: 'credentials',
            id: 'signup',
            credentials: {
                username: { label: 'username', type: 'text' },
                email: { label: 'email', type: 'text' },
                first_name: { label: 'first_name', type: 'text' },
                last_name: { label: 'last_name', type: 'text' },
                password: { label: 'password', type: 'password' },
            },
            async authorize(credentials) {
                const data = await create(credentials)
                return data
            },
        }),
    ],
    debug: process.env.NODE_ENV === 'development',
    session: {
        maxAge: 30 * 24 * 60 * 60,
    },
    pages: {
        signIn: '/login',
    },
    secret: 'fdsvfsdgergf',
    callbacks: {
        async signIn({ user, credentials }: any) {
            credentials.callbackUrl = '/'
            return true
        },
        async redirect({ url, baseUrl }) {
            console.log(url)
            if (url.startsWith('/')) return `${baseUrl}${url}`
            else if (new URL(url).origin === baseUrl) return url
            return baseUrl
        },
        async jwt({ token, user }) {
            if (user) {
                token = { ...user }
            }
            return token
        },
        async session({ session, token, user }: any) {
            session.token = token.token
            return session
        },
    },
}
