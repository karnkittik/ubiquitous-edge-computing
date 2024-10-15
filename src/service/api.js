import axios from 'axios'
import config from '../configs/config'
import {
    SageMakerRuntimeClient,
    InvokeEndpointCommand,
} from '@aws-sdk/client-sagemaker-runtime'

//Edge API
const edgeApi = axios.create({
    baseURL: `${config.edgeUrl}/`,
    headers: {
        'Content-Type': 'application/json',
    },
})
edgeApi.interceptors.request.use((x) => {
    x.meta = x.meta || {}
    x.meta.requestStartedAt = new Date().getTime()
    return x
})
edgeApi.interceptors.response.use(
    (x) => {
        x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt
        return x
    },
    (err) => {
        throw err
    }
)

//Cloud API
const client = new SageMakerRuntimeClient({
    region: config.cloudRegion,
    credentials: {
        accessKeyId: config.cloudAccessKeyID,
        secretAccessKey: config.cloudSecretAccessKey,
    },
})
const InvokeEndpoint = (base64Image) => {
    const params = {
        EndpointName: config.cloudEndpointName,
        ContentType: 'text/csv',
        Body: base64Image,
    }

    return new Promise(async (resolve, reject) => {
        const requestStartedAt = new Date().getTime()
        try {
            const command = new InvokeEndpointCommand(params)
            const response = await client.send(command)
            const responseTime = new Date().getTime() - requestStartedAt
            const responseData = await new Response(response.Body).text()
            console.log('Response from SageMaker:', responseData)
            console.log('Response time (ms):', responseTime)

            resolve({ responseData, responseTime })
        } catch (error) {
            console.error('Error invoking endpoint:', error)
            reject(error)
        }
    })
}

const queryService = {
    edgePeopleCounting(base64Image, modelSize) {
        // MockTest;
        return new Promise((resolve, reject) => {
            setTimeout(
                () =>
                    resolve({
                        data: { building: 'A', floor: '1', tag: '21' },
                        responseTime: 235.5,
                    }),
                1000
            )
        })
        return cloudApi.post('/get-location', {
            building_id: fps[qId - 1].b_id,
            finger_print: fps[qId - 1].fp,
        })
    },
    cloudPeopleCounting(base64Image) {
        // MockTest;
        return new Promise((resolve, reject) => {
            setTimeout(
                () =>
                    resolve({
                        data: { building: 'A', floor: '1', tag: '21' },
                        responseTime: 235.5,
                    }),
                1000
            )
        })
        return InvokeEndpoint(base64Image)
    },
}
export default queryService
