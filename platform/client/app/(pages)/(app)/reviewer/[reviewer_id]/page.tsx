import React from 'react'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/app/utils/authOptions'
import { getUserInfo, getUserPastPublications } from '@/app/api/usersAPI'
import { Title, UnstyledButton } from '@mantine/core'

const page = async ({
    params: { reviewer_id },
}: {
    params: { reviewer_id: string }
}) => {
    const session: any = await getServerSession(authOptions)
    const user = await getUserInfo(
        { user_id: reviewer_id },
        { token: session.token }
    )
    const pastPublications: any = await getUserPastPublications(
        { user_id: reviewer_id },
        { token: session.token }
    )
    return (
        <div className='w-full'>
            <Title order={2} mt={20}>
                {user.first_name} {user.last_name}
            </Title>
            <div className='rounded-lg border bg-slate-100 p-6 mt-5'>
                <Title order={3} mb={8}>
                    Past Publications
                </Title>
                <div className='flex flex-col gap-3 overflow-auto h-[70vh] pr-2'>
                    {pastPublications.map((pastPublication: any, i: number) => (
                        <div
                            key={i}
                            className='rounded-lg border bg-white p-4 w-full'
                        >
                            <Title order={5}>{pastPublication.title}</Title>
                            <div className='text-sm mt-2'>
                                <span className='font-semibold'>Abstract </span>{' '}
                                {pastPublication.abstract}{' '}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default page
