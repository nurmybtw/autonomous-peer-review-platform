import React from 'react'
import {
    Badge,
    Button,
    Center,
    Group,
    Title,
    UnstyledButton,
} from '@mantine/core'
import Link from 'next/link'

const IncomingReviewRequests = ({
    myIncomingReviewRequests,
    profile,
}: {
    myIncomingReviewRequests: any
    profile: any
}) => {
    return (
        <div className='rounded-lg bg-slate-100 w-full px-6 py-4 mt-8 border'>
            <Title order={3} mb={5}>
                Review requests
            </Title>
            <div className='w-full overflow-x-auto flex gap-3 mt-5'>
                {myIncomingReviewRequests.length > 0 ? (
                    myIncomingReviewRequests.map((revreq: any, i: number) => (
                        <UnstyledButton
                            key={i}
                            className=''
                            component={Link}
                            href={`/review_requests/${revreq.id}/`}
                        >
                            <div className='rounded-lg border bg-white p-4 w-[240px]'>
                                <Title order={5}>
                                    {revreq.submission.title}
                                </Title>
                                <div className='flex mt-2 gap-2 flex-wrap'>
                                    {revreq.submission.categories.map(
                                        (category: any, j: number) => (
                                            <Badge key={`${i}_${j}`}>
                                                {category}
                                            </Badge>
                                        )
                                    )}
                                </div>
                            </div>
                        </UnstyledButton>
                    ))
                ) : (
                    <div className='w-full py-10'>
                        <Center>
                            {profile.is_reviewer ? (
                                <div className=''>No review requests</div>
                            ) : (
                                <div className='w-[400px] text-center'>
                                    You are currently designated as a
                                    non-reviewer. <br /> If you wish to review
                                    papers, please change your reviewing status
                                    in the profile settings.
                                </div>
                            )}
                        </Center>
                    </div>
                )}
            </div>
        </div>
    )
}

export default IncomingReviewRequests
