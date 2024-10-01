import React from 'react'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/app/utils/authOptions'
import {
    acceptReviewRequest,
    getReviewRequest,
    rejectReviewRequest,
} from '@/app/api/reviewrequests.api'
import {
    Title,
    Text,
    Breadcrumbs,
    Badge,
    Group,
    Center,
    Button,
} from '@mantine/core'
import ReviewRequestDecision from './components/ReviewRequestDecision'
import PaperDetails from '../../components/PaperDetails'

const page = async ({
    params: { revreq_id },
}: {
    params: { revreq_id: string }
}) => {
    const session: any = await getServerSession(authOptions)
    const reviewRequest = await getReviewRequest(
        { revreq_id },
        { token: session.token }
    )

    return (
        <div className='w-full'>
            <PaperDetails submission={reviewRequest.submission} />
            <ReviewRequestDecision
                revreq_id={revreq_id}
                submission_id={reviewRequest.submission.id}
                token={session.token}
            />
        </div>
    )
}

export default page
