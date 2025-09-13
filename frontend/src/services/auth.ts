import { api } from "./api"


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

	// save token in localstorage
	localStorage.setItem("token", res.data.access_token);
	localStorage.setItem("user", res.data)
	return res.data;
}


export const getCurrentUser = async () => {
	const res = await api.get("/users/me")
}











