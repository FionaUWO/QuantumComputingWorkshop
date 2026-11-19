// Prefix a site-relative path with the deployment base (/QuantumComputingWorkshop).
const base = import.meta.env.BASE_URL.replace(/\/$/, '');
export const url = (path = '') => `${base}/${path.replace(/^\//, '')}`;
