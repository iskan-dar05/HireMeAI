import { Navigate } from "react-router-dom"
import { jwtDecode } from "jwt-decode"

export const isTokenValid = () => {
	try{
		const token = localStorage.getItem("access_token")
		const decode = jwtDecode(token);
		const now = Date.now() / 1000
		return decode.exp && decode.exp > now;
	} catch{
		return false
	}
}


export const ProtectedRoute = ({ children }) => {
	

	if(!isTokenValid()){
		return <Navigate to="/login" replace />;
	}

	return children;
};

