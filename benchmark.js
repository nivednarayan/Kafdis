import http from 'k6/http';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
    vus: 50,
    duration: '30s'
};

export default function(){
    const clientId = `user:${randomIntBetween(1, 10000)}`;
    http.post("http://localhost:8080/check", 
        JSON.stringify({ 'client_id' : clientId, 'limit' : 1000, 'window_seconds' : 60}),
        { headers: {'Content-Type' : 'application/json'} }
    )
}
