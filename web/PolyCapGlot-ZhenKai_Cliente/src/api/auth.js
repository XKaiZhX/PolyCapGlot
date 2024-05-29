import axios from './axios_instance.js';
import { jwtDecode } from "jwt-decode";

const API = 'http://127.0.0.1:9002';

export const RegisterRequest = user => axios.post(API + '/user/', user);
export const LoginRequest = user => axios.post(API + '/user/login', user);

export const UpdateUsernameRequest = (user, token) => axios.put(API + '/user/update/username', user, {
    header: { 'x-access-token': token }
});

export const UpdatePasswordRequest = (user, token) => axios.put(API + '/user/update/password', user, {
    header: { 'x-access-token': token }
});

export const DeleteUserRequest = (email, token) => axios.delete(API + '/user/' + email, {
    header: { 'x-access-token': token }
});

export const requestVideo = (videoData, token) => axios.post(API + '/video/request', videoData, {
    headers: { 'x-access-token': token }
});


export const uploadVideoRequest = (videoData, token) => axios.post(API + '/video/upload', videoData, {
    headers: { 'x-access-token': token }
});

export const requestUserVideos = (token) => axios.post(API + '/video/user', {}, {
    headers: { 'x-access-token': token } 
});

export const requestUserPerfil = (email, token) => axios.get(API + `/user/${email}`, {
    headers: { 'x-access-token': token }
});

  