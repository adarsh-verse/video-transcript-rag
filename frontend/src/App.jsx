import { useState } from "react"
import { ProcessInput } from "./services/api"
import { askQuestion } from "./services/api";

function App() {
  const [file, setFile] = useState(null)
  const [url, setUrl] = useState("");

  const [loading, setLoading] = useState(false)
  const [processed, setProcessed] = useState(false)

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);

  const handleProcess = async () => {
    if (!file && !url) {
      alert("Upload file or enter URl")
      return;
    }

    try {
      setLoading(true)
      setProcessed(false)

      console.log("before process")
      await ProcessInput(file, url);
      console.log("after process")
      setProcessed(true)
    }
    catch (error) {
      alert("Processing failed")
    }
    finally {
      setLoading(false)
    }
  }

  const handleAsk = async () => {
    if (!question) {
      alert("Enter a question");
      return;
    }

    try {
      setLoading(true)

      const data = await askQuestion(question);

      setAnswer(data)
    }
    catch (error) {
      alert("Error getting answer")
    }
    finally {
      setLoading(false)
    }
  }



  return (
    <div className="min-h-screen bg-linear-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center px-4">

      <h1 className="text-4xl font-bold mb-8 text-gray-800">
        RAG App 🚀
      </h1>

      <div className="backdrop-blur-md bg-white/70 p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-200">

        {/* FILE INPUT */}
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4 w-full text-sm text-gray-700
             file:mr-4 file:py-2 file:px-4
             file:rounded-lg file:border-0
             file:text-sm file:font-semibold
             file:bg-blue-500 file:text-white
             hover:file:bg-blue-600 transition"
        />

        <p className="text-center text-gray-500 mb-2">OR</p>


        <input
          type="text"
          placeholder="Paste URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full p-3 border rounded-xl mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />


        <button
          onClick={handleProcess}
          className="w-full bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-600 transition font-semibold"
        >
          Process
        </button>

        {loading && (
          <p className="text-center mt-4 text-blue-500 font-medium animate-pulse">
            Processing...
          </p>
        )}

        {processed && (
          <p className="text-green-600 text-center mt-4 font-medium">
            ✅ Processed Successfully
          </p>
        )}

        {processed && (
          <div className="mt-6 w-full max-w-md">

            <input
              type="text"
              placeholder="Ask question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full p-3 border rounded-xl mb-4 focus:outline-none focus:ring-2 focus:ring-green-400"
            />

            <button
              onClick={handleAsk}
              className="w-full bg-green-500 text-white py-3 rounded-xl hover:bg-green-600 transition font-semibold disabled:opacity-50"
            >
              {loading ? "Thinking..." : "Ask Question"}
            </button>

          </div>
        )}

        {answer && (
          <div className="bg-white/80 backdrop-blur-md p-6 mt-6 rounded-2xl shadow-lg w-full max-w-md border border-gray-200">

            <h2 className="font-semibold text-lg mb-3 text-gray-800">
              💡 Answer
            </h2>

            <p className="text-gray-700 mb-4 leading-relaxed">
              {answer.answer}
            </p>

            <div className="bg-gray-50 p-3 rounded-lg text-sm text-gray-600">

              <div className="flex items-center gap-2 mb-1">
                <span>📺</span>
                <span className="truncate">{answer.video_title}</span>
              </div>

              <div className="flex items-center gap-2">
                <span>⏱</span>
                <span>{answer.timestamp}</span>
              </div>

            </div>

          </div>
        )}


      </div>

    </div>
  );
}

export default App
