import client from './client'

export default {
  /**
   * 获取所有示例数据
   */
  getAllExamples() {
    return client.get('/api/examples')
  },
  
  /**
   * 获取指定ID的示例数据
   * @param {string} id - 示例数据ID
   */
  getExampleById(id) {
    return client.get(`/api/examples/${id}`)
  },
  
  /**
   * 获取当前用户创建的示例数据
   */
  getMyExamples() {
    return client.get('/api/examples/my')
  },
  
  /**
   * 创建新的示例数据
   * @param {Object} exampleData - 示例数据
   */
  createExample(exampleData) {
    return client.post('/api/examples', exampleData)
  },
  
  /**
   * 更新示例数据
   * @param {string} id - 示例数据ID
   * @param {Object} exampleData - 要更新的示例数据
   */
  updateExample(id, exampleData) {
    return client.put(`/api/examples/${id}`, exampleData)
  },
  
  /**
   * 删除示例数据
   * @param {string} id - 示例数据ID
   */
  deleteExample(id) {
    return client.delete(`/api/examples/${id}`)
  }
}
