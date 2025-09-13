import { useLocation } from "react-router-dom"


const ResumeViewer = ()=>{
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const pdfUrl = queryParams.get("url");

	if(!pdfUrl)
	{
		return <p className="text-center mt-10 text-red-500">No PDF to show</p>;
	}

	return (
		<div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Your Generated Resume</h1>

      <div className="w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">
        <iframe
          src={pdfUrl}
          title="Resume PDF"
          className="w-full h-[80vh]"
        ></iframe>
      </div>

      <a
        href={pdfUrl}
        download="resume.pdf"
        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
      >
        Download PDF
      </a>
    </div>
	)
}

export default ResumeViewer

