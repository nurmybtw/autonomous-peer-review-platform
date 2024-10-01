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
import { getSubmission } from '@/app/api/submissions.api'
import ReviewTextArea from './components/ReviewTextArea'
import PaperDetails from '../../components/PaperDetails'

const page = async ({
    params: { submission_id },
}: {
    params: { submission_id: string }
}) => {
    const session: any = await getServerSession(authOptions)
    const submission = await getSubmission(
        { submission_id },
        { token: session.token }
    )

    return (
        <div className='w-full'>
            <PaperDetails submission={submission} />
            <ReviewTextArea
                submission_id={submission_id}
                token={session.token}
            />
        </div>
    )
}

export default page
