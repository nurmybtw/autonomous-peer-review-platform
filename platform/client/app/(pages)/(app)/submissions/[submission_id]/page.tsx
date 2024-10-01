import React from 'react'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/app/utils/authOptions'
import {
    getSubmission,
    getSubmissionReviews,
    getSubmissionReviewRequests,
} from '@/app/api/submissions.api'
import {
    Title,
    Text,
    Breadcrumbs,
    Badge,
    Group,
    Center,
    UnstyledButton,
    Button,
} from '@mantine/core'
import PaperDetails from '../../components/PaperDetails'
import Link from 'next/link'
import ReviewRequests from './components/ReviewRequests'

const page = async ({
    params: { submission_id },
}: {
    params: { submission_id: string }
}) => {
    const session: any = await getServerSession(authOptions)
    const submission: any = await getSubmission(
        { submission_id },
        { token: session.token }
    )
    const reviewRequests = await getSubmissionReviewRequests(
        { submission_id },
        { token: session.token }
    )
    const reviews = await getSubmissionReviews(
        { submission_id },
        { token: session.token }
    )

    return (
        <div className='w-full'>
            <PaperDetails submission={submission} />
            <div className='rounded-lg bg-slate-100 border p-6 mt-5'>
                <Title order={3} mb={8}>
                    Reviews
                </Title>
                <div className='flex flex-col gap-3'>
                    {reviews.length > 0 ? (
                        reviews.map((review: any, i: number) => (
                            <div
                                key={i}
                                className='rounded-lg border bg-white w-full p-4'
                            >
                                <Title order={5} mb={3}>
                                    Review {i + 1} from{' '}
                                    {review.reviewer.first_name}{' '}
                                    {review.reviewer.last_name}
                                </Title>
                                <Text>{review.content}</Text>
                            </div>
                        ))
                    ) : (
                        <div className='w-full py-10'>
                            <Center>
                                <div className=''>
                                    No reviews were submitted yet :(
                                </div>
                            </Center>
                        </div>
                    )}
                </div>
            </div>
            <ReviewRequests
                reviewRequests={reviewRequests}
                submission_id={submission_id}
                token={session.token}
            />
        </div>
    )
}

export default page
