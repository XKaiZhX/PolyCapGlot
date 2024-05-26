import { jwtDecode } from "jwt-decode";

const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkxvY2FsQGxvY2FsLmNvbSIsInVzZXJuYW1lIjoiTG9jYWwiLCJleHAiOiIyMDI0LTA1LTI2IDAzOjI3OjAyLjAzNTI0MSJ9.QzCb13yN7Zv7pXyAN5JtaTqcEcN_IhXvNS3c4B_08p0";
const decodedToken = jwtDecode(token);

function obtenerTiempoActual() {
    const fecha = new Date();
    const año = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    const horas = String(fecha.getHours()).padStart(2, '0');
    const minutos = String(fecha.getMinutes()).padStart(2, '0');
    const segundos = String(fecha.getSeconds()).padStart(2, '0');
    const milisegundos = String(fecha.getMilliseconds()).padStart(6, '0');

    return `${año}-${mes}-${dia} ${horas}:${minutos}:${segundos}.${milisegundos}`;
}

const tiempoActual = obtenerTiempoActual();
console.log(tiempoActual);

console.log(decodedToken.exp);

if (decodedToken.exp >  tiempoActual) {
    console.log("1")
}

if (decodedToken.exp <  tiempoActual) {
    console.log("1")
}