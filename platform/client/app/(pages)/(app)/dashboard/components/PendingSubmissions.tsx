'use client'

import React from 'react'
import Link from 'next/link'

import {
    Badge,
    Button,
    Center,
    Group,
    Title,
    UnstyledButton,
    Modal,
} from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'

import { IconPlus } from '@tabler/icons-react'
import SubmissionForm from './SubmissionForm'

const PendingSubmissions = ({
    mySubmissions,
    token,
}: {
    mySubmissions: any
    token: string
}) => {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <div className='rounded-lg bg-slate-100 w-full px-6 py-4 mt-8 border'>
            <Modal
                opened={opened}
                onClose={close}
                title={<Title order={3}>Submission Box</Title>}
                centered
                size='auto'
                radius='md'
            >
                <SubmissionForm token={token} closeModal={close} />
            </Modal>
            <Group justify='space-between'>
                <Title order={3} mb={5}>
                    My pending submissions
                </Title>
                <Button
                    variant='light'
                    size='compact-sm'
                    leftSection={<IconPlus size={15} />}
                    onClick={open}
                >
                    Add submission
                </Button>
            </Group>
            <div className='w-full overflow-x-auto flex gap-3 mt-5 pb-3'>
                {mySubmissions.length > 0 ? (
                    mySubmissions.map((submission: any, i: number) => (
                        <UnstyledButton
                            key={i}
                            className=''
                            component={Link}
                            href={`/submissions/${submission.id}/`}
                        >
                            <div className='rounded-lg border bg-white p-4 w-[240px]'>
                                <Title order={5}>{submission.title}</Title>
                                <div className='flex mt-2 gap-2 flex-wrap'>
                                    {submission.categories.map(
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
                            {<div className=''>No pending submissions</div>}
                        </Center>
                    </div>
                )}
            </div>
        </div>
    )
}

export default PendingSubmissions
