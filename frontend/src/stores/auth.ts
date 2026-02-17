import { ref } from 'vue'
import { defineStore } from 'pinia'
import UserService from "@/services/userService"
import type { UserBase } from '@/types/user'

const useAuthStore = defineStore('auth', () => {
    const loggedIn = ref(false)
    const user = ref<UserBase | null>(null)

    const checkAuth = async () => {
        try {
            const userData = await UserService.getMe()
            user.value = userData
            loggedIn.value = true
        } catch {
            loggedIn.value = false
            user.value = null
        } 
    }

    const setLoggedIn = (value: boolean) => {
        loggedIn.value = value
    }

    return { loggedIn, user, checkAuth, setLoggedIn }
})

export default useAuthStore
