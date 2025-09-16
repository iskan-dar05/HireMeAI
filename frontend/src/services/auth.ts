import { api } from "./axios"


export interface RegisterData {
	firstname: string,
	lastname: string,
	email: string
	password: string
}


export interface LoginData {
	email: string,
	passsword: string
}

export const register = async (data: RegisterData) => {
	const res = await api.post("/auth/register", data);
	return res.data
};


export const login = async (data: LoginData) => {
	const res = await api.post("/auth/login", data);
	return res.data;
}


export const logout = async () => {
	const res = await api.post("/auth/logout", {});
	console.log(res.data)
}

export const getCurrentUser = async () => {
	const res = await api.get("/users/me")
}











