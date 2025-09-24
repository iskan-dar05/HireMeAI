import { api } from "./axios"


export interface FormData{
	fullname: string,
	email: string,
	phone: string,
	location: string,
	profession: string,
	passion: string,
	experience: string,
	job_desc: string,
	skills: string,
	education: string
}


export const createResume = async (data: FormData)=>{
	const res = await api.post("/resume/create-resume", data)
	return res.data
}

export const fetchResumes = async () => {
	const res = await api.get("resume/fetch-resumes"



