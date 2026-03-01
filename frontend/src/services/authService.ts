import api from './api.ts'
import { config } from '@/config'


export default class AuthService {
    static async login(username: string, password: string) {
        const form = new URLSearchParams({ username: username, password: password })
        const res = await api.post("/auth/token", form, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        localStorage.setItem("accessToken", res.data.access_token);
        return res.data
    }

    static async googleLogin() {
        window.location.href = `${config.apiUrl}/auth/google/login`;
    }

    static async sendEmailCode(receiver: string) {
        const res = await api.post("/auth/send/email-code?receiver=" + encodeURIComponent(receiver))
        return res.data
    }

    static async logout() {
        await api.delete("/auth/logout")
        localStorage.removeItem("accessToken")
    }
}
