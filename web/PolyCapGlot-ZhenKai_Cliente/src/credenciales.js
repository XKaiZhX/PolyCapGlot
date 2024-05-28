// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getStorage } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBSBnO-zBvz0ZfPCDcxDCjymZEV12UetQ4",
    authDomain: "polycapglot-d87cf.firebaseapp.com",
    projectId: "polycapglot-d87cf",
    storageBucket: "polycapglot-d87cf.appspot.com",
    messagingSenderId: "124381084935",
    appId: "1:124381084935:web:cd57310d1a7837e99ad9a2"
};

// Initialize Firebase
const appFirebase = initializeApp(firebaseConfig);
const analytics = getAnalytics(appFirebase);

const storage = getStorage(appFirebase);

export { appFirebase, storage };
