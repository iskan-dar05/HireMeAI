import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { api } from "@/services/axios"

const ResumeViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");

  const [pdfBlobUrl, setPdfBlobUrl] = useState<string | null>(null);

  useEffect(()=>{
    if(pdfUrl)
  })

}