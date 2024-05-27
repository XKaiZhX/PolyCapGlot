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
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST

interface ApiService {
    @GET("android")
    suspend fun testRequest(): String

    @POST("user/")
    suspend fun registerRequest(@Body data: RegisterData): Response<UserDataDTO>

    @POST("user/login")
    suspend fun login(@Body request: LoginData): Response<LoginResponse>

    @POST("video/user")
    suspend fun requestVideos(@Header("x-access-token") token: String): Response<List<MenuViewModel.Video>>

    @POST("video/request")
    suspend fun videoRequest(
        @Header("x-access-token") token: String,
        @Body request: VideoRequestData
    ): Response<VideoResponseData>

    @POST("video/upload")
    suspend fun uploadVideo(
        @Header("x-access-token") token: String,
        @Body request: UploadRequestData
    ): Response<UploadResponseData>
}