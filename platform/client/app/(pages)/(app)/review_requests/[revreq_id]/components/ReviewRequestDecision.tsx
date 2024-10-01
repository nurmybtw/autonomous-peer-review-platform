'use client'

import React from 'react'
import {
    Title,
    Text,
    Breadcrumbs,
    Badge,
    Group,
    Center,
    Button,
} from '@mantine/core'
import { useRouter } from 'next/navigation'
import { useSession } from 'next-auth/react'
import {
    acceptReviewRequest,
    rejectReviewRequest,
} from '@/app/api/reviewrequests.api'

const ReviewRequestDecision = ({
    revreq_id,
    submission_id,
    token,
}: {
    revreq_id: string
    submission_id: string
    token: string
}) => {
    const router = useRouter()
    // const { data: session, status }: any = useSession()
    return (
        <div className='rounded-lg bg-slate-100 border p-6 mt-5'>
            <Group justify='space-between'>
                <Title order={3} mb={5}>
                    Are you willing to review this paper?
                </Title>
                <Group gap={10}>
                    <Button
                        color='green'
                        onClick={async () => {
                            await acceptReviewRequest({ revreq_id }, { token })
                            router.push(`/submit_review/${submission_id}/`)
                        }}
                    >
                        Accept
                    </Button>
                    <Button
                        color='red'
                        onClick={async () => {
                            await rejectReviewRequest({ revreq_id }, { token })
                            router.push('/dashboard/')
                        }}
                    >
                        Reject
                    </Button>
                </Group>
            </Group>
        </div>
    )
}

export default ReviewRequestDecision
