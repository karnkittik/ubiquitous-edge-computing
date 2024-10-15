const config = {
    edgeUrl: process.env.VUE_APP_EDGE_URL || '',
    cloudRegion: process.env.VUE_APP_CLOUD_REGION || '',
    cloudAccessKeyID: process.env.VUE_APP_ACCESS_KEY_ID || '',
    cloudSecretAccessKey: process.env.VUE_APP_SECRET_ACCESS_KEY || '',
    cloudEndpointName: process.env.VUE_APP_ENDPOINT_NAME || '',
}

console.log('===========')
console.log(config)
console.log('===========')

export default config
