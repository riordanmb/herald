export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <div className="text-center">
          <h1 className="text-6xl font-serif font-bold text-heraldic-azure mb-4">
            Herald
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Heraldic Manuscript Management System
          </p>
          <div className="text-left max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Features</h2>
            <ul className="space-y-2 text-gray-700">
              <li>📜 Manuscript cataloging with multi-surrogate support</li>
              <li>🛡️ Heraldic markup according to the laws of heraldry</li>
              <li>⚖️ Cross-manuscript arms comparison</li>
              <li>🌳 Manuscript recession tracking (stemma visualization)</li>
              <li>✍️ Text transcription with paleographic features</li>
              <li>🔍 Advanced heraldic search</li>
              <li>🤖 ML-powered scribal hand similarity analysis</li>
            </ul>
            <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Status:</strong> Phase 1 - Foundation <br />
                <strong>Version:</strong> 0.1.0-alpha <br />
                <strong>Backend API:</strong> <code>http://localhost:8000/api/v1/</code>
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
