import api from '@/app/api/axios'

const getMySubmissions = async (credentials: any, status: any = null) => {
    try {
        const res = await api.get(
            `/submissions/my_submissions/?status=${status ? status : ''}`,
            {
                headers: {
                    Authorization: `Token ${credentials.token}`,
                },
            }
        )
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const createSubmission = async (submission: any, credentials: any) => {
    try {
        const res = await api.post('/submissions/', submission, {
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: `Token ${credentials.token}`,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getSubmission = async (params: any, credentials: any) => {
    try {
        const res = await api.get(`/submissions/${params.submission_id}/`, {
            headers: {
                Authorization: `Token ${credentials.token}`,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getSubmissionReviewRequests = async (params: any, credentials: any) => {
    try {
        const res = await api.get(
            `/submissions/${params.submission_id}/review_requests/`,
            {
                headers: {
                    Authorization: `Token ${credentials.token}`,
                },
            }
        )
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getSubmissionReviews = async (params: any, credentials: any) => {
    try {
        const res = await api.get(
            `/submissions/${params.submission_id}/reviews/`,
            {
                headers: {
                    Authorization: `Token ${credentials.token}`,
                },
            }
        )
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const submitReview = async (data: any, params: any, credentials: any) => {
    try {
        const res = await api.post(
            `/submissions/${params.submission_id}/submit_review/`,
            data,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Token ${credentials.token}`,
                },
            }
        )
        return res.data
    } catch (err) {
        console.log(err)
    }
}

export {
    createSubmission,
    getSubmission,
    getMySubmissions,
    getSubmissionReviewRequests,
    getSubmissionReviews,
    submitReview,
}
