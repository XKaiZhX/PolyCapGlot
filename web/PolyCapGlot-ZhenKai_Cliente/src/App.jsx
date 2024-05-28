import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { AuthProvider } from './context/AuthContext.jsx'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Login } from './components/LoginPage.jsx'
import { Main } from './components/MainPage.jsx'
import { Register } from './components/RegisterPage.jsx';
import { VideoRequestPage } from './components/PreUploadPage.jsx'; 
import { Processing } from './components/ProcessingPage.jsx'
import { VideoPlayer } from './components/VideoPlayerPage.jsx';
import { VideoList } from './components/VideoListPage.jsx';
import { UserPerfil } from './components/UserPerfilPage.jsx';
import { UpdateUsernamePage } from './components/UpdateUsernamePage.jsx'
import { UpdatePasswordPage } from './components/UpdatePasswordPage.jsx';

function App() {

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Login/>}/>
          <Route path='/register' element={<Register/>}/>
          <Route path='/preupload' element={<VideoRequestPage/>}/>
          <Route path='/main/:folder/:fileName/:fileExtension' element={<Main/>}/>
          <Route path='/processing/:fileName/:language' element={<Processing/>}/>
          <Route path="/videoplayer/:folder/:fileName/:fileExtension" element={<VideoPlayer />} />
          <Route path='/misvideos' element={<VideoList/>}/>
          <Route path='/perfil/:email' element={<UserPerfil/>}/>
          <Route path='/updateusername' element={<UpdateUsernamePage/>}/>
          <Route path='/updatepassword' element={<UpdatePasswordPage/>}/>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
    
  )
}

export default App
