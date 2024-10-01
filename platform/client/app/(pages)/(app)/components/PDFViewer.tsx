'use client'
import React from 'react'
import { Worker, SpecialZoomLevel, Viewer } from '@react-pdf-viewer/core'
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout'
import '@react-pdf-viewer/default-layout/lib/styles/index.css'

const PDFViewer = ({ file }: { file: any }) => {
    const defaultLayoutPluginInstance: any = defaultLayoutPlugin()

    return (
        <div style={{ width: '80vw', height: '78vh' }}>
            <Worker workerUrl='https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js'>
                <Viewer
                    fileUrl={file}
                    defaultScale={SpecialZoomLevel.PageWidth}
                    plugins={[defaultLayoutPluginInstance]}
                />
            </Worker>
        </div>
    )
}

export default PDFViewer
