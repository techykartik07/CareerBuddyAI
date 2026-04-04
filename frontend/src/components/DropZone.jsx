import { useDropzone } from 'react-dropzone'

export default function DropZone({ onFileSelect, selectedFile }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    onDrop: (files) => onFileSelect(files[0])
  })

  return (
    <div {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
        ${isDragActive   ? 'border-purple-500 bg-purple-50'
        : selectedFile   ? 'border-green-400 bg-green-50'
        :                  'border-gray-200 hover:border-purple-300'}`}>
      <input {...getInputProps()} />
      {selectedFile ? (
        <div>
          <p className="text-green-600 font-medium">{selectedFile.name}</p>
          <p className="text-gray-400 text-sm mt-1">Click or drop to replace</p>
        </div>
      ) : (
        <div>
          <p className="text-gray-500">Drag your resume PDF here</p>
          <p className="text-gray-400 text-sm mt-1">or click to browse</p>
        </div>
      )}
    </div>
  )
}