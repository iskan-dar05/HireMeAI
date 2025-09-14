import { Navigate } from "react-router-dom"
import { jwtDecode } from "jwt-decode"

const isTokenValid = (token) => {
	try{
		const decode = jwtDecode(token);
		const now = Date.now() / 1000
		return decode.exp && decode.exp > now;
	} catch{
		return false
	}
}


const ProtectedRoute = ({ children }) => {
	const token = localStorage.getItem("token")

	if(!token || !isTokenValid(token)){
		return <Navigate to="/login" replace />;
	}

	return children;
};

export default ProtectedRoute;