import { ref } from 'vue'
import { defineStore } from 'pinia'
import UserService from "@/services/userService"

const useAuthStore = defineStore('auth', () => {
    const loggedIn = ref(false)

    const checkAuth = async () => {
        try {
            await UserService.getMe()
            loggedIn.value = true
        } catch {
            loggedIn.value = false
        } 
    }

    const setLoggedIn = (value: boolean) => {
        loggedIn.value = value
    }

    return { loggedIn, checkAuth, setLoggedIn }
})

export default useAuthStore
