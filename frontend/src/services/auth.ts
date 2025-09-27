import { api } from "./axios"


export interface RegisterData {
	firstname: string,
	lastname: string,
	email: string
	password: string
}


export interface LoginData {
	email: string,
	password: string
}

export const scheduleTokenRefresh = (token: string) => {
	try{
		const payload = JSON.parse(atob(token.split(".")[1]));
		const expiry = payload.exp * 1000;
		const now = Date.now();

		const timeout = expiry - now - 60000;

		if (timeout > 0) {
			setTimeout(refreshAccessToken, timeout);
		}
	}catch(err)
	{
		console.error("Invalid token:", err)
	}
	
}

export const refreshAccessToken = async () => {
	const refreshToken = localStorage.getItem("refresh_token")

	if(!refreshToken) return;

	try{
		const res = await api.post("/auth/refresh",
		{
			refresh_token: refreshToken
		}
		)

		const data = res.data
	    localStorage.setItem("access_token", data.access_token);

	    // Schedule next refresh
	    scheduleTokenRefresh(data.access_token);
	}catch(err)
	{
		console.error("Refresh token failed", err);
	}
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
	const refreshToken = localStorage.getItem("refresh_token")
	const res = await api.post("/auth/logout", {
		refresh_token: refreshToken
	});
	localStorage.removeItem("access_token")
	localStorage.removeItem("refresh_token")
	console.log(res.data)
}

export const getCurrentUser = async () => {
	const res = await api.get("/users/me")
}











