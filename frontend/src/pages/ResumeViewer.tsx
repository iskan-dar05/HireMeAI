import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { api } from "@/services/axios"; // your axios instance with token interceptor

const ResumeViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");

  const [pdfBlobUrl, setPdfBlobUrl] = useState<string | null>(null);

  useEffect(() => {
    if (pdfUrl) {
      const fetchPdf = async () => {
        try {
          const res = await api.get(pdfUrl, { responseType: "blob" }); 
          const blob = new Blob([res.data], { type: "application/pdf" });
          const url = URL.createObjectURL(blob);
          setPdfBlobUrl(url);
        } catch (err) {
          console.error("Failed to load PDF:", err);
        }
      };
      fetchPdf();
    }
  }, [pdfUrl]);

  if (!pdfUrl) {
    return <p className="text-center mt-10 text-red-500">No PDF to show</p>;
  }

  return (
    <div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Your Generated Resume</h1>

      {pdfBlobUrl ? (
        <div className="w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">
          <iframe src={pdfBlobUrl} title="Resume PDF" className="w-full h-[80vh]" />
        </div>
      ) : (
        <p>Loading PDF...</p>
      )}

      {pdfBlobUrl && (
        <a
          href={pdfBlobUrl}
          download="resume.pdf"
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
        >
          Download PDF
        </a>
      )}
    </div>
  );
}

export default ResumeViewer;
