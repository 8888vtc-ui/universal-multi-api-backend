'use client'

import { useState } from 'react'
import { Download, FileJson, FileText, FileSpreadsheet } from 'lucide-react'

interface ExportButtonProps {
  data: any
  filename?: string
}

export default function ExportButton({ data, filename = 'export' }: ExportButtonProps) {
  const [showMenu, setShowMenu] = useState(false)

  const exportJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}.json`
    a.click()
    URL.revokeObjectURL(url)
    setShowMenu(false)
  }

  const exportCSV = () => {
    // Simple CSV conversion
    const csv = Object.entries(data)
      .map(([key, value]) => `${key},${JSON.stringify(value)}`)
      .join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}.csv`
    a.click()
    URL.revokeObjectURL(url)
    setShowMenu(false)
  }

  const exportMarkdown = () => {
    const md = `# ${filename}\n\n\`\`\`json\n${JSON.stringify(data, null, 2)}\n\`\`\``
    const blob = new Blob([md], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}.md`
    a.click()
    URL.revokeObjectURL(url)
    setShowMenu(false)
  }

  return (
    <div className="relative">
      <button
        onClick={() => setShowMenu(!showMenu)}
        className="btn-secondary flex items-center gap-2"
      >
        <Download className="w-4 h-4" />
        Exporter
      </button>

      {showMenu && (
        <div className="absolute right-0 mt-2 glass rounded-xl p-2 shadow-xl border border-dark-700/50 z-50">
          <button
            onClick={exportJSON}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
          >
            <FileJson className="w-4 h-4" />
            <span className="text-sm">JSON</span>
          </button>
          <button
            onClick={exportCSV}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span className="text-sm">CSV</span>
          </button>
          <button
            onClick={exportMarkdown}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
          >
            <FileText className="w-4 h-4" />
            <span className="text-sm">Markdown</span>
          </button>
        </div>
      )}
    </div>
  )
}





