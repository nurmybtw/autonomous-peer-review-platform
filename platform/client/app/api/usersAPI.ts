import api from '@/app/api/axios'

const getProfile = async (credentials: any) => {
    try {
        const res = await api.get('/users/profile/', {
            headers: {
                Authorization: `Token ${credentials.token}`,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const create = async (user: any) => {
    try {
        const res = await api.post('/users/', user)
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getUserInfo = async (params: any, credentials: any) => {
    try {
        const res = await api.get(`/users/${params.user_id}/`, {
            headers: {
                Authorization: `Token ${credentials.token}`,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getUserPastPublications = async (params: any, credentials: any) => {
    try {
        const res = await api.get(
            `/users/${params.user_id}/past_publications/`,
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

export { create, getUserInfo, getProfile, getUserPastPublications }
