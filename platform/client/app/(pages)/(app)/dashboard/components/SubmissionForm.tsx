'use client'

import React from 'react'
import {
    Button,
    Center,
    FileInput,
    PasswordInput,
    Textarea,
    TextInput,
} from '@mantine/core'
import { useForm, isEmail, hasLength } from '@mantine/form'
import { createSubmission } from '@/app/api/submissions.api'
import { useRouter } from 'next/navigation'
import { IconFileTypePdf } from '@tabler/icons-react'

const SubmissionForm = ({
    token,
    closeModal,
}: {
    token: string
    closeModal: any
}) => {
    const router = useRouter()
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: { title: '', abstract: '', file: null },
    })

    const submit = async (values: any) => {
        await createSubmission(
            {
                title: values.title,
                abstract: values.abstract,
                content_file: values.file,
            },
            { token }
        )
        closeModal()
        router.refresh()
    }

    return (
        <form onSubmit={form.onSubmit(submit)}>
            <div className='flex-col min-w-[720px]'>
                <TextInput
                    {...form.getInputProps('title')}
                    key={form.key('title')}
                    mt='lg'
                    placeholder='Title'
                    label='Title'
                />
                <Textarea
                    {...form.getInputProps('abstract')}
                    key={form.key('abstract')}
                    mt='lg'
                    placeholder='Abstract'
                    label='Abstract'
                    rows={10}
                />
                <FileInput
                    {...form.getInputProps('file')}
                    key={form.key('file')}
                    accept='application/pdf'
                    clearable
                    label='Upload PDF'
                    placeholder='Upload PDF'
                    leftSection={<IconFileTypePdf size={20} />}
                    mt='lg'
                />
                <Button type='submit' mt='lg' fullWidth variant='filled'>
                    Submit
                </Button>
            </div>
        </form>
    )
}

export default SubmissionForm
