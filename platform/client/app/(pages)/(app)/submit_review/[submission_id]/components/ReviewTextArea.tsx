'use client'

import React, { useState } from 'react'
import {
    Title,
    Text,
    Breadcrumbs,
    Badge,
    Group,
    Center,
    Button,
    Textarea,
} from '@mantine/core'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { submitReview } from '@/app/api/submissions.api'

const ReviewTextArea = ({
    submission_id,
    token,
}: {
    submission_id: string
    token: string
}) => {
    const router = useRouter()
    const [reviewText, setReviewText] = useState('')
    return (
        <div className='rounded-lg bg-slate-100 border p-6 mt-5 mb-8'>
            <Textarea
                resize='vertical'
                label='Write your review here'
                placeholder='Your review'
                autosize
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                minRows={10}
                mb={20}
            />
            <Button
                onClick={async () => {
                    await submitReview(
                        { content: reviewText },
                        { submission_id },
                        { token }
                    )
                    router.push('/dashboard/')
                }}
            >
                Submit review
            </Button>
        </div>
    )
}

export default ReviewTextArea
