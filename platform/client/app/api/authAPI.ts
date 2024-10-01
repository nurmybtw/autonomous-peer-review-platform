import api from '@/app/api/axios'

const signin = async (user: any) => {
    try {
        const res = await api.post('/api-token-auth/', user)
        return res.data
    } catch (err) {
        console.log(err)
    }
}

export { signin }
