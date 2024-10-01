import React from 'react'
import Layout from './components/Layout'

const layout = ({ children }: { children: React.ReactNode }) => {
    return (
        <div className='px-[160px] min-h-screen'>
            <Layout>{children}</Layout>
        </div>
    )
}

export default layout
