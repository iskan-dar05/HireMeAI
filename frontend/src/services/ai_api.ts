import { api } from "./api"


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


export const createCV = async (data: FormData)=>{
	const res = await api.post("/ai/create-resume", data)
	return res.data
}





