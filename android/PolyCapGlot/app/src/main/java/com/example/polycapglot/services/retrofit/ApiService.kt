package com.example.polycapglot.services.retrofit

import com.example.polycapglot.services.retrofit.models.LoginData
import com.example.polycapglot.services.retrofit.models.LoginResponse
import com.example.polycapglot.services.retrofit.models.RegisterData
import com.example.polycapglot.services.retrofit.models.UploadRequestData
import com.example.polycapglot.services.retrofit.models.UploadResponseData
import com.example.polycapglot.services.retrofit.models.UserDataDTO
import com.example.polycapglot.services.retrofit.models.VideoRequestData
import com.example.polycapglot.services.retrofit.models.VideoResponseData
import com.example.polycapglot.ui.viewmodel.MenuViewModel
import com.example.polycapglot.ui.viewmodel.models.Video
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

interface ApiService {

    @POST("user/")
    suspend fun registerRequest(@Body data: RegisterData): Response<UserDataDTO>

    @POST("user/login")
    suspend fun loginRequest(@Body request: LoginData): Response<LoginResponse>

    @POST("video/user")
    suspend fun videosRequest(@Header("x-access-token") token: String): Response<List<Video>>

    @POST("video/request")
    suspend fun uploadVideoPrerequest(
        @Header("x-access-token") token: String,
        @Body request: VideoRequestData
    ): Response<VideoResponseData>

    @POST("video/upload")
    suspend fun uploadVideoRequest(
        @Header("x-access-token") token: String,
        @Body request: UploadRequestData
    ): Response<UploadResponseData>
}