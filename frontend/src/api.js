import axios from 'axios'

// API base URL - change this for production
const API_URL = import.meta.env.VITE_API_URL || 'https://hrms-lite-backend-twn4.onrender.com'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Employee APIs
export const getEmployees = () => api.get('/api/employees')
export const getEmployee = (employeeId) => api.get(`/api/employees/${employeeId}`)
export const createEmployee = (data) => api.post('/api/employees', data)
export const deleteEmployee = (employeeId) => api.delete(`/api/employees/${employeeId}`)

// Attendance APIs
export const getAllAttendance = () => api.get('/api/attendance')
export const getEmployeeAttendance = (employeeId) => api.get(`/api/attendance/${employeeId}`)
export const markAttendance = (data) => api.post('/api/attendance', data)

// Dashboard
export const getDashboard = () => api.get('/api/dashboard')

export default api
