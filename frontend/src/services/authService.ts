import api from './api.ts'


export default class AuthService {
    static async login(username: string, password: string) {
        const form = new URLSearchParams({username: username, password: password})
        const res = await api.post("/auth/token", form, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        localStorage.setItem("accessToken", res.data.access_token);
        return res.data
    }
}