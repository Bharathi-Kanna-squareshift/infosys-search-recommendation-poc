import { init as initApm } from '@elastic/apm-rum'

const apm = initApm({
    serviceName: 'infosys-Demo',
    serverUrl: 'https://1bb02e2b8a054de080d0c0e3eefa5417.apm.us-central1.gcp.cloud.es.io:443', 
    environment: 'dev',
    serviceVersion: '1.0.0',
    pageLoadTraceId: true,
    pageLoadSpanId: true,
    pageLoadSampled: true,
  })

  
export default apm