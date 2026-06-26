import { useAuthStore } from '@/stores/auth'

const BASE_URL = 'http://localhost:8000'


export const signin = async (email, password) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await fetch(`${BASE_URL}/auth/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        credentials: 'include',
        body: formData
    })

    if (!response.ok) {
        throw new Error("Email ou senha incorretos.")
    }

    return await response.json() // { access_token, token_type }
}

export const signup = async (email, username, password, role) => {
    const payload = {
        email: email,
        username: username,
        password: password,
        role: role
    }

    const response = await fetch(`${BASE_URL}/auth`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(payload)
    })

    if (!response.ok) {
        const errorBody = await response.json()
        const errorMessage = errorBody.detail
        throw new Error(errorMessage)
    }
}

export const refreshAccessToken = async () => {
    try {
        const response = await fetch(`${BASE_URL}/auth/refresh`, {
            method: 'POST',
            credentials: 'include'
        })

        if (!response.ok) {
            throw new Error('Sessão expirada')
        }

        const data = await response.json()
        return data.access_token
    } catch (error) {
        return null
    }
}

export const fetchComAuth = async (url, options = {}) => {
    const authStore = useAuthStore()

    let response = await fetch(`${BASE_URL}${url}`, {
        ...options,
        credentials: 'include',
        headers: {
            ...options.headers,
            Authorization: `Bearer ${authStore.accessToken}`
        }
    })

    if (response.status === 401) {
        const novoToken = await refreshAccessToken()

        if (!novoToken) {
            authStore.logout()
            throw new Error('Sessão expirada, faça login novamente')
        }

        authStore.setAccessToken(novoToken)

        response = await fetch(`${BASE_URL}${url}`, {
            ...options,
            credentials: 'include',
            headers: {
                ...options.headers,
                Authorization: `Bearer ${novoToken}`
            }
        })
    }

    return response
}