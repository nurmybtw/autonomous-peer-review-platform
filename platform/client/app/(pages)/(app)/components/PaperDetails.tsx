'use client'

import React from 'react'
import { Title, Text, Badge, Group, Button, Modal } from '@mantine/core'
import { IconFileTypePdf } from '@tabler/icons-react'
import { useDisclosure } from '@mantine/hooks'
import PDFViewer from './PDFViewer'

const PaperDetails = ({ submission }: { submission: any }) => {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <div className='w-full'>
            <Modal
                opened={opened}
                onClose={close}
                centered
                size='auto'
                radius='md'
                title={<Title order={3}>Full Text</Title>}
            >
                <PDFViewer file={submission.content_file} />
            </Modal>
            <Title order={1} mt={20}>
                {submission.title}
            </Title>
            <div className='rounded-lg bg-slate-100 border p-6 mt-5'>
                <Group justify='space-between'>
                    <Title order={3} mb={5}>
                        Paper details
                    </Title>
                    <Button
                        variant='subtle'
                        leftSection={<IconFileTypePdf size={20} />}
                        onClick={() => open()}
                    >
                        PDF
                    </Button>
                </Group>
                <div className='w-full'>
                    <Title order={5}>Abstract</Title>
                    <Text>{submission.abstract}</Text>
                </div>
                <div className='w-full mt-3'>
                    <Title order={5}>Topical Categories</Title>
                    <div className='flex mt-2 gap-2 flex-wrap'>
                        {submission.categories.map(
                            (category: any, j: number) => (
                                <Badge key={`${j}`}>{category}</Badge>
                            )
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PaperDetails
