import React from 'react'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/app/utils/authOptions'
import { getProfile } from '@/app/api/usersAPI'
import { getMySubmissions } from '@/app/api/submissions.api'
import {
    Badge,
    Button,
    Center,
    Group,
    Title,
    UnstyledButton,
} from '@mantine/core'
import { getMyReviewRequests } from '@/app/api/reviewrequests.api'
import PendingSubmissions from './components/PendingSubmissions'
import IncomingReviewRequests from './components/IncomingReviewRequests'

const page = async () => {
    const session: any = await getServerSession(authOptions)
    const profile = await getProfile({ token: session.token })
    const mySubmissions = await getMySubmissions(
        { token: session.token },
        'pending'
    )
    const myIncomingReviewRequests = await getMyReviewRequests(
        { token: session.token },
        'pending'
    )

    return (
        <div className='mt-5'>
            <Title>Welcome, {profile.first_name}!</Title>
            <PendingSubmissions
                mySubmissions={mySubmissions}
                token={session.token}
            />
            <IncomingReviewRequests
                myIncomingReviewRequests={myIncomingReviewRequests}
                profile={profile}
            />
        </div>
    )
}

export default page
