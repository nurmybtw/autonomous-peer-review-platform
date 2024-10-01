'use client'

import React from 'react'
import { Title, Badge, Group, UnstyledButton, Button } from '@mantine/core'
import { notifications } from '@mantine/notifications'
import Link from 'next/link'
import { IconUser, IconUserSearch } from '@tabler/icons-react'
import { newReviewerRequest } from '@/app/api/reviewrequests.api'

const statusColorMap: any = {
    accepted: 'green',
    rejected: 'red',
    pending: 'orange',
}
const ReviewRequests = ({
    reviewRequests,
    submission_id,
    token,
}: {
    reviewRequests: any
    submission_id: any
    token: any
}) => {
    return (
        <div className='rounded-lg bg-slate-100 border p-6 mt-5 mb-8'>
            <Title order={3} mb={8}>
                Review requests
            </Title>
            <div className='flex flex-col gap-3'>
                {reviewRequests.map((reviewRequest: any, i: number) => (
                    <div
                        key={i}
                        className='rounded-lg border bg-white w-full p-4'
                    >
                        <Group justify='space-between'>
                            <Group>
                                <Title order={5}>
                                    {reviewRequest.reviewer.first_name}{' '}
                                    {reviewRequest.reviewer.last_name}
                                </Title>
                                <Badge
                                    color={statusColorMap[reviewRequest.status]}
                                >
                                    {reviewRequest.status}
                                </Badge>
                            </Group>
                            <Group>
                                <Button
                                    component={Link}
                                    variant='light'
                                    leftSection={<IconUser size={20} />}
                                    href={`/reviewer/${reviewRequest.reviewer.id}`}
                                >
                                    View profile
                                </Button>
                                {reviewRequest.status === 'pending' ? (
                                    <Button
                                        variant='light'
                                        leftSection={
                                            <IconUserSearch size={20} />
                                        }
                                        onClick={async () => {
                                            await newReviewerRequest(
                                                { submission_id },
                                                { token }
                                            )
                                            notifications.show({
                                                title: 'Success',
                                                message:
                                                    'New review request was sent',
                                                color: 'green',
                                            })
                                        }}
                                    >
                                        Request new reviewer
                                    </Button>
                                ) : (
                                    <></>
                                )}
                            </Group>
                        </Group>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default ReviewRequests
