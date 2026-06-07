const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // 开发端口（可通过环境变量 PORT 覆盖）
    port: Number(process.env.PORT) || 80,
    // 对外提供服务：允许从服务器/局域网访问
    host: '0.0.0.0',
    // 避免通过 IP/域名访问时触发 host 校验问题
    allowedHosts: 'all',
    // 允许跨域（主要用于 vue-cli devServer 场景；生产环境需在你的 nginx/网关配置）
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
      'Access-Control-Max-Age': '86400'
    }
  }
})
