import api from '@/app/api/axios'

const getMyReviewRequests = async (credentials: any, status: any = null) => {
    try {
        const res = await api.get(
            `/review_requests/my_requests/?status=${status ? status : ''}`,
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

const getReviewRequest = async (params: any, credentials: any) => {
    try {
        const res = await api.get(`/review_requests/${params.revreq_id}`, {
            headers: {
                Authorization: `Token ${credentials.token}`,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const acceptReviewRequest = async (params: any, credentials: any) => {
    try {
        const res = await api.post(
            `/review_requests/${params.revreq_id}/accept/`,
            { temp: 'temp' },
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

const rejectReviewRequest = async (params: any, credentials: any) => {
    try {
        const res = await api.post(
            `/review_requests/${params.revreq_id}/reject/`,
            {},
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

const newReviewerRequest = async (params: any, credentials: any) => {
    try {
        const res = await api.post(
            `/submissions/${params.submission_id}/new_reviewer_request/`,
            {},
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

export {
    getMyReviewRequests,
    getReviewRequest,
    acceptReviewRequest,
    rejectReviewRequest,
    newReviewerRequest,
}
