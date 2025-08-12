import axios from '@/utils/axios'

export default {
  get(url, params = {}) {
    return axios.get(url, { params })
  },
  
  post(url, data = {}) {
    return axios.post(url, data)
  },
  
  put(url, data = {}) {
    return axios.put(url, data)
  },
  
  delete(url) {
    return axios.delete(url)
  }
}
