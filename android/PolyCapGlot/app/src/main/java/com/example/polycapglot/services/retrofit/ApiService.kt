package com.example.polycapglot.services.retrofit

import com.example.polycapglot.services.retrofit.models.LoginData
import com.example.polycapglot.services.retrofit.models.LoginResponse
import com.example.polycapglot.services.retrofit.models.RegisterData
import com.example.polycapglot.services.retrofit.models.UpdatePasswordRequestData
import com.example.polycapglot.services.retrofit.models.UpdateUsernameRequestData
import com.example.polycapglot.services.retrofit.models.UploadRequestData
import com.example.polycapglot.services.retrofit.models.UploadResponseData
import com.example.polycapglot.services.retrofit.models.UserDataDTO
import com.example.polycapglot.services.retrofit.models.VideoRequestData
import com.example.polycapglot.services.retrofit.models.VideoResponseData
import com.example.polycapglot.ui.viewmodel.models.Video
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.PUT

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

    @DELETE("/video/")
    suspend fun deleteVideo(
        @Header("x-access-token") token: String,
        @Header("video-id") videoId: String
    ): Response<Boolean>

    @DELETE("/video/translation")
    suspend fun deleteTranslation(
        @Header("x-access-token") token: String,
        @Header("trans_id") transId: String,
        @Header("video_id") videoId: String,
    ): Response<Boolean>

    @DELETE("user/")
    suspend fun deleteUser(@Header("x-access-token") token: String): Response<Boolean>

    @PUT("user/update/username")
    suspend fun updateUsername(
        @Header("x-access-token") token: String,
        @Body request: UpdateUsernameRequestData
    ): Response<Void>

    @PUT("user/update/password")
    suspend fun updatePassword(
        @Header("x-access-token") token: String,
        @Body request: UpdatePasswordRequestData
    ): Response<Void>
}